# Generated by Django 3.0.8 on 2020-08-07 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0003_auto_20200801_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipes',
            name='pipe_size',
            field=models.CharField(max_length=30),
        ),
    ]
