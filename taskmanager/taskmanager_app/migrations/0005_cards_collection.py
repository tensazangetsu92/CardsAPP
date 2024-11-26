# Generated by Django 5.1.1 on 2024-10-08 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager_app', '0004_cards_cardscollections_delete_taskmanagerdb'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='collection',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='taskmanager_app.cardscollections'),
        ),
    ]
