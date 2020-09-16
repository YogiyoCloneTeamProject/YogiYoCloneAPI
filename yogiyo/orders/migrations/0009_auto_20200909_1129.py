# Generated by Django 3.1 on 2020-09-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20200909_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('현금', 'Cash'), ('신용카드', 'Creditcard'), ('요기서결제', 'Yogiyo Pay')], max_length=10),
        ),
    ]