# Generated by Django 3.0.3 on 2020-02-27 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_contact_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='description',
            field=models.CharField(blank='No description', max_length=600, null='True'),
        ),
    ]
