# Generated by Django 4.2.2 on 2023-06-16 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RareUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('profile_image_url', models.CharField(max_length=50)),
                ('created_on', models.DateField()),
                ('active', models.BooleanField()),
                ('uid', models.CharField(max_length=50)),
            ],
        ),
    ]
