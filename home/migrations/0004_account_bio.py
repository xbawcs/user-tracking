# Generated by Django 4.2.6 on 2023-10-12 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
