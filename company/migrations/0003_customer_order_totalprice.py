# Generated by Django 4.0.3 on 2022-03-25 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_order',
            name='totalprice',
            field=models.CharField(default='', max_length=100),
        ),
    ]
