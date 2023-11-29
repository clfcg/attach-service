# Generated by Django 4.2.7 on 2023-11-28 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attach', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetViewDataAttachPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_request_id', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('op_token', models.CharField(max_length=50)),
                ('poll_file', models.FileField(null=True, upload_to='poll/%Y/%m/%d/')),
                ('user', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=15)),
            ],
        ),
    ]