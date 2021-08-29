# Generated by Django 3.1.4 on 2021-02-07 12:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20210207_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitations',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=False),
        ),
    ]
