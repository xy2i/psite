# Generated by Django 2.2.2 on 2019-07-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190708_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(default='are you gay nigga'),
            preserve_default=False,
        ),
    ]
