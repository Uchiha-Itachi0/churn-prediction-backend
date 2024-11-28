from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MLModel
from .serializers import MLModelSerializer
from .task import train_model
import uuid


class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the model instance
        instance = serializer.save()

        # Start training task
        train_model.delay(str(instance.id))

        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['model_id'] = str(instance.id)

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )