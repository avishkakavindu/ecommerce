# Generated by Django 4.2.10 on 2024-03-23 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0010_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.CharField(max_length=200),
        ),
    ]
