from django.db import models
import uuid


class MLModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    accuracy = models.FloatField(null=True, blank=True)
    csv_content = models.JSONField(null=True, blank=True)  # Add this field to store CSV data
    training_metrics = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.created_at}"
