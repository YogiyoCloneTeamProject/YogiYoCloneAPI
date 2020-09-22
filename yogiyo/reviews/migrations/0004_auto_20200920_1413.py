# Generated by Django 3.1 on 2020-09-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_review_order_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='order_menu',
            field=models.CharField(max_length=50),
        ),
    ]
