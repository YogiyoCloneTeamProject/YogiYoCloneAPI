# Generated by Django 3.1 on 2020-08-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0014_merge_20200828_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='caption',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, max_length=400, null=True, upload_to='menu_image'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='option',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
