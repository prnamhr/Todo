# Generated by Django 5.0.2 on 2024-03-15 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_task_delete_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
