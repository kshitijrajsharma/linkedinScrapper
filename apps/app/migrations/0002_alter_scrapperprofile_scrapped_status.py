# Generated by Django 3.2.6 on 2021-09-10 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapperprofile',
            name='scrapped_status',
            field=models.BooleanField(default=False),
        ),
    ]
