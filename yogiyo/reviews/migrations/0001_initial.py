# Generated by Django 3.1 on 2020-09-17 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=300)),
                ('rating', models.PositiveIntegerField()),
                ('taste', models.PositiveIntegerField()),
                ('delivery', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='review_image')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=300)),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
            ],
        ),
    ]
