# Generated by Django 3.1 on 2020-09-24 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20200924_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewcomment',
            name='review',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reviews.review'),
        ),
        migrations.AlterField(
            model_name='reviewimage',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='reviews.review'),
        ),
    ]
