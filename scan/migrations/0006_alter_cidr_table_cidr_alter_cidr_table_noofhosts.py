# Generated by Django 4.2.5 on 2023-09-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0005_alter_cidr_table_cidr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidr_table',
            name='cidr',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='cidr_table',
            name='noOFhosts',
            field=models.CharField(max_length=4),
        ),
    ]
