# Generated by Django 2.0.4 on 2018-04-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibData', '0009_remove_book_bookurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='bownum',
            field=models.IntegerField(default=0),
        ),
    ]
