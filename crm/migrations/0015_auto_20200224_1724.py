# Generated by Django 3.0.3 on 2020-02-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_auto_20200224_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='avatar',
            field=models.ImageField(null=True, upload_to=None),
        ),
    ]
