# Generated by Django 3.1 on 2020-09-20 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20200917_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='order_menu',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
