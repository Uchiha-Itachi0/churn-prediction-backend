import tensorflow as tf
from keras import layers, models
from keras.callbacks import Callback

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ModelTrainer:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback

    def create_model(self, input_shape):
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=input_shape),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])

        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        return model

    def train(self, X_train, X_test, y_train, y_test, epochs=10):
        model = self.create_model((X_train.shape[1],))

        class ProgressCallback(Callback):
            def __init__(self, progress_callback):
                super().__init__()
                self.progress_callback = progress_callback

            def on_epoch_end(self, epoch, logs=None):
                progress = int((epoch + 1) / self.params['epochs'] * 100)
                if self.progress_callback:
                    self.progress_callback(progress)

        callback = ProgressCallback(self.progress_callback)

        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=[callback],
            verbose=0
        )

        return model, history
