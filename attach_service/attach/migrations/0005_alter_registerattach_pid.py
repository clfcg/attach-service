# Generated by Django 4.2.7 on 2023-12-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attach', '0004_statusattach_registerattach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerattach',
            name='pid',
            field=models.IntegerField(null=True),
        ),
    ]
