# Generated by Django 4.2.6 on 2023-10-12 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='application',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='application',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='application',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='device',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='device',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='device',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='device',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='devicelog',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='devicelog',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='devicelog',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='devicelog',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='devicelog',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.application'),
        ),
        migrations.AddField(
            model_name='devicelog',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.device'),
        ),
    ]
