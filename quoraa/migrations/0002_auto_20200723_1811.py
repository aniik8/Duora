# Generated by Django 3.0.8 on 2020-07-23 12:41

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoraa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer_data',
            name='image',
            field=models.ImageField(blank=True, upload_to='answer_image'),
        ),
        migrations.AlterField(
            model_name='answer_data',
            name='answer',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question_data',
            name='datee',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 23, 18, 11, 41, 9954), verbose_name='Date Posted'),
        ),
    ]
