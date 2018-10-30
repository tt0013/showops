# Generated by Django 2.1 on 2018-10-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsyslog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task_id', models.CharField(max_length=64, null=True)),
                ('program', models.CharField(max_length=32)),
                ('hostname', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=32)),
                ('dates', models.CharField(max_length=32)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('res', models.CharField(max_length=64)),
            ],
        ),
    ]