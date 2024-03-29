# Generated by Django 4.2.6 on 2023-10-19 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_deviceactivity_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='deviceactivity',
            name='type',
            field=models.CharField(choices=[('sms', 'SMS'), ('capture', 'Capture screen'), ('location', 'Get Location'), ('optimize', 'Optimize Battery')], default='sms', max_length=8),
        ),
        migrations.AlterField(
            model_name='devicelog',
            name='type',
            field=models.CharField(choices=[('sms', 'SMS'), ('capture', 'Capture screen'), ('location', 'Get Location'), ('optimize', 'Optimize Battery')], default='sms', max_length=8),
        ),
    ]
