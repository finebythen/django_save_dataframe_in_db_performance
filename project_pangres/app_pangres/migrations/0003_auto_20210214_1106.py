# Generated by Django 3.1.6 on 2021-02-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pangres', '0002_uploadmodeldemo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodeldemo',
            name='upload_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]