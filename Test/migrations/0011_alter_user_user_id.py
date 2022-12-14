# Generated by Django 4.0 on 2022-11-22 08:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0010_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('34e5bc9b-d7d8-4df3-bbf9-335a2f42744f'), primary_key=True, serialize=False, unique=True),
        ),
    ]
