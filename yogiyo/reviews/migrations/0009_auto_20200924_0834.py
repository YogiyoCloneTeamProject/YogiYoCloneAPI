# Generated by Django 3.1 on 2020-09-24 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20200924_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewcomment',
            name='review',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='reviews.review'),
        ),
    ]