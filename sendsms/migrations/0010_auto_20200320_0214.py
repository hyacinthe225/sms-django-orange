# Generated by Django 2.2.1 on 2020-03-20 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendsms', '0009_auto_20200320_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sms',
            name='address',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
