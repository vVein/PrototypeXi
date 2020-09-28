# Generated by Django 3.1.1 on 2020-09-20 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0011_auto_20200903_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipes',
            name='design_gradient',
            field=models.DecimalField(decimal_places=3, default=0.01, max_digits=10),
        ),
        migrations.AddField(
            model_name='pipes',
            name='upstream_structure_drop_structure',
            field=models.BooleanField(default=False),
        ),
    ]