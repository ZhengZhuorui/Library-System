# Generated by Django 2.0.4 on 2018-05-03 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LibData', '0012_auto_20180503_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('com', models.CharField(default='', max_length=2018)),
                ('bookisbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LibData.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LibData.Member')),
            ],
        ),
    ]
