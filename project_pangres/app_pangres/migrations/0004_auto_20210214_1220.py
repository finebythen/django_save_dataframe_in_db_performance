# Generated by Django 3.1.6 on 2021-02-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pangres', '0003_auto_20210214_1106'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadModel',
        ),
        migrations.AlterField(
            model_name='uploadmodeldemo',
            name='age',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='uploadmodeldemo',
            name='upload_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
