# Generated by Django 5.0.4 on 2024-04-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0005_progresslog_completed_alter_progresslog_billed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='start',
        ),
        migrations.AddField(
            model_name='challenge',
            name='provider',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='title',
            field=models.TextField(null=True),
        ),
    ]
