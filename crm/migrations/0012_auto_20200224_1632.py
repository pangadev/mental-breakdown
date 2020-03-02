# Generated by Django 3.0.3 on 2020-02-24 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_contact_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='description',
            field=models.CharField(default='No description', max_length=600, null='True'),
            preserve_default='True',
        ),
        migrations.AlterField(
            model_name='contact',
            name='sex',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Unsure', 'Unsure')], default='Unknown', max_length=64, null=True),
        ),
    ]