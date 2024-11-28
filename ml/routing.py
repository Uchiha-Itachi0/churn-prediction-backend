from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/training/(?P<model_id>[\w-]+)/$',
        consumers.TrainingProgressConsumer.as_asgi()
    ),
]