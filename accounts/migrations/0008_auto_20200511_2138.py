# Generated by Django 3.0.4 on 2020-05-11 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200511_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='pic',
            field=models.ImageField(default='media/img_sample/avatar.png', upload_to='proimage'),
        ),
    ]
