# Generated by Django 3.0.4 on 2020-05-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_attendance_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='pic',
            field=models.ImageField(default='img_sample/avatar.png', upload_to='proimage'),
        ),
    ]
