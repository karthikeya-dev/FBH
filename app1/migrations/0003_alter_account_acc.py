# Generated by Django 5.1.7 on 2025-04-09 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_account_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='acc',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
