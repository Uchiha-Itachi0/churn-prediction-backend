# Generated by Django 4.2.16 on 2024-11-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlmodel',
            name='file',
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='csv_content',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
