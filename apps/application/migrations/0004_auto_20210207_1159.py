# Generated by Django 3.1.4 on 2021-02-07 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0003_auto_20210207_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='grouprelationships',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.group'),
        ),
        migrations.AlterField(
            model_name='grouprelationships',
            name='user_statistics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.statistics'),
        ),
        migrations.AlterField(
            model_name='invitations',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.group'),
        ),
        migrations.AlterField(
            model_name='invitations',
            name='user_statistics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.statistics'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
