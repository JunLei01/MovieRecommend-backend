# Generated by Django 3.2.13 on 2022-07-02 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MRApp', '0002_registerinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scoreinformation',
            fields=[
                ('eva_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('movie_score', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'scoreinformation',
                'managed': False,
            },
        ),
    ]
