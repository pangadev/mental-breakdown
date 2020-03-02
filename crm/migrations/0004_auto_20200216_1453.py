# Generated by Django 3.0.3 on 2020-02-16 14:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_relationshiptype_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='date',
        ),
        migrations.AddField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
