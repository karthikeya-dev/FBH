# Generated by Django 5.1.7 on 2025-04-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_account_acc'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]
