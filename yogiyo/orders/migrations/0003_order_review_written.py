# Generated by Django 3.1 on 2020-09-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200917_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='review_written',
            field=models.BooleanField(default=False),
        ),
    ]