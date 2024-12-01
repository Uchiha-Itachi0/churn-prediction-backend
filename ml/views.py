from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MLModel
from .serializers import MLModelSerializer
from .task import train_model
from .pagination import CSVContentPagination
import pandas as pd


class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
    pagination_class = CSVContentPagination

    def create(self, request):
        uploaded_file = request.FILES.get('file', None)

        if not uploaded_file:
            return Response(
                {'error': 'File is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and save the MLModel instance (without file)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        try:
            # Process the file in-memory
            df = pd.read_csv(uploaded_file)
            csv_content = df.to_dict(orient='records')

            # Save CSV content to the model instance
            instance.csv_content = csv_content
            instance.save()

            # Trigger the training task with the data
            train_model.delay(instance.id, df.to_dict())

            return Response(
                {
                    **serializer.data,
                    'model_id': str(instance.id),
                    'csv_content': csv_content[:self.pagination_class.page_size]  # Send first 20 records
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        # Retrieve model details along with csv_content if training is completed
        model = self.get_object()

        response_data = {
            'id': model.id,
            'name': model.name,
            'status': model.status,
            'accuracy': model.accuracy,
        }

        if model.status == 'completed':
            paginator = CSVContentPagination()
            page = paginator.paginate_queryset(model.csv_content, request)
            if page is not None:
                paginated_response = paginator.get_paginated_response(page).data
                response_data.update(paginated_response)
                return Response(response_data)  # Explicitly return a Response object

            # If no pagination, just return the full data
            response_data['csv_content'] = model.csv_content  # Full content if pagination isn't used
            return Response(response_data)  # Explicitly return a Response object
        else:
            return Response({
                'id': model.id,
                'status': model.status,
                'message': 'Model training is in progress.'
            })

