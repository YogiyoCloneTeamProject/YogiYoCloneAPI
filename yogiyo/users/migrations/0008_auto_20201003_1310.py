# Generated by Django 3.1 on 2020-10-03 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0008_auto_20201002_0618'),
        ('users', '0007_auto_20200928_0537'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('user', 'restaurant')},
        ),
    ]
