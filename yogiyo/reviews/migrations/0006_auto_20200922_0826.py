# Generated by Django 3.1 on 2020-09-22 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200917_0725'),
        ('reviews', '0005_auto_20200920_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
