# Generated by Django 4.0.4 on 2022-10-21 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0003_userdata_foll_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='poster',
            name='caption',
            field=models.TextField(default='The Guy Has Not Setted Any Caption For This Post So Now This is The Property of Polynet Official Thank you :)'),
        ),
    ]
