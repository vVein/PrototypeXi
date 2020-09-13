# Generated by Django 3.0.8 on 2020-08-02 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_auto_20200728_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upstream_node', models.CharField(max_length=20)),
                ('downstream_node', models.CharField(max_length=20)),
                ('pipe_size', models.CharField(max_length=20)),
                ('downstreamInvert', models.DecimalField(decimal_places=3, max_digits=19)),
            ],
        ),
        migrations.RenameField(
            model_name='structures',
            old_name='size',
            new_name='type_and_size',
        ),
        migrations.RemoveField(
            model_name='structures',
            name='type',
        ),
        migrations.AlterField(
            model_name='structures',
            name='databaseKey',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='structures',
            name='surface_elevation',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
