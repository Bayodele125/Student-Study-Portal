# Generated by Django 4.0.3 on 2022-06-03 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_diary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
