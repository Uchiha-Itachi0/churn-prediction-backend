from celery import shared_task
import pandas as pd
from .utils.preprocessor import DataPreprocessor
from .utils.model_trainer import ModelTrainer
from .models import MLModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


@shared_task
def train_model(model_id, data):
    from django.utils.log import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Starting training for model_id: {model_id}")
    ml_model = MLModel.objects.get(id=model_id)

    try:
        # Read data
        df = pd.DataFrame.from_dict(data)

        # Preprocess data
        preprocessor = DataPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.preprocess(df)

        # Define a progress sender function
        def send_progress(progress):
            async_to_sync(channel_layer.group_send)(
                f"training_{model_id}",  # Use the same group name format as in consumer
                {
                    'type': 'training_progress',
                    'progress': progress
                }
            )

        # Train model
        trainer = ModelTrainer(send_progress)
        model, history = trainer.train(X_train, X_test, y_train, y_test)

        # Update model status and accuracy
        ml_model.status = 'completed'
        ml_model.accuracy = float(history.history['val_accuracy'][-1])
        ml_model.save()

    except Exception as e:
        logger.error(f"Training failed for model_id {model_id}: {str(e)}")
        ml_model.status = 'failed'
        ml_model.save()
        raise e
