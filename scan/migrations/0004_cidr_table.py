# Generated by Django 4.2.5 on 2023-09-24 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0003_ip_results_snmp'),
    ]

    operations = [
        migrations.CreateModel(
            name='cidr_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidr', models.CharField(max_length=2)),
                ('noOFhosts', models.CharField(max_length=3)),
            ],
        ),
    ]