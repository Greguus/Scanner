# Generated by Django 4.2.5 on 2023-09-24 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0007_alter_cidr_table_noofhosts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cidr_table',
            options={'managed': False},
        ),
    ]
