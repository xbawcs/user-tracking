# Generated by Django 4.2.6 on 2023-10-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_device_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicelog',
            name='image',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='devicelog',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
