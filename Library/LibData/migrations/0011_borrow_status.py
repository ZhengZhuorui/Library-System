# Generated by Django 2.0.4 on 2018-04-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibData', '0010_member_bownum'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
