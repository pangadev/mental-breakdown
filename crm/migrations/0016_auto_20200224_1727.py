# Generated by Django 3.0.3 on 2020-02-24 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_auto_20200224_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='avatar',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
