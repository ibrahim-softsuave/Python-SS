# Generated by Django 4.0 on 2022-11-16 11:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('e24d0079-95c3-4154-a99b-a05c81f45df6'), primary_key=True, serialize=False, unique=True),
        ),
    ]