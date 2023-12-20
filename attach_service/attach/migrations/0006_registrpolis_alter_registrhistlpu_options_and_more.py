# Generated by Django 4.2.7 on 2023-12-19 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attach', '0005_alter_registerattach_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrPolis',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dedit', models.DateTimeField(blank=True, db_column='DEDIT', null=True)),
                ('q', models.CharField(blank=True, db_column='Q', max_length=5, null=True)),
                ('qogrn', models.CharField(blank=True, db_column='QOGRN', max_length=15, null=True)),
                ('prz', models.CharField(blank=True, db_column='PRZ', max_length=8, null=True)),
                ('spol', models.CharField(blank=True, db_column='SPOL', max_length=20, null=True)),
                ('npol', models.CharField(blank=True, db_column='NPOL', max_length=20, null=True)),
                ('poltp', models.IntegerField(blank=True, db_column='POLTP', null=True)),
                ('polvid', models.IntegerField(blank=True, db_column='POLVID', null=True)),
                ('dbeg', models.DateTimeField(blank=True, db_column='DBEG', null=True)),
                ('dend', models.DateTimeField(blank=True, db_column='DEND', null=True)),
                ('rstop', models.IntegerField(blank=True, db_column='RSTOP', null=True)),
                ('dstop', models.DateTimeField(blank=True, db_column='DSTOP', null=True)),
                ('dstop_cs', models.DateTimeField(blank=True, db_column='DSTOP_CS', null=True)),
                ('st', models.IntegerField(blank=True, db_column='ST', null=True)),
                ('del_field', models.BooleanField(blank=True, db_column='DEL', null=True)),
                ('okato', models.CharField(blank=True, db_column='OKATO', max_length=11, null=True)),
                ('nvs', models.CharField(blank=True, db_column='NVS', max_length=9, null=True)),
                ('dvs', models.DateTimeField(blank=True, db_column='DVS', null=True)),
                ('et', models.DateTimeField(blank=True, db_column='ET', null=True)),
                ('unload', models.DateTimeField(blank=True, db_column='UNLOAD', null=True)),
                ('dz', models.DateTimeField(blank=True, db_column='DZ', null=True)),
                ('dp', models.DateTimeField(blank=True, db_column='DP', null=True)),
                ('dh', models.DateTimeField(blank=True, db_column='DH', null=True)),
                ('err', models.CharField(blank=True, db_column='ERR', max_length=200, null=True)),
                ('oldpid', models.IntegerField(blank=True, db_column='OLDPID', null=True)),
                ('sout', models.DateTimeField(blank=True, db_column='SOUT', null=True)),
                ('m2id', models.IntegerField(blank=True, db_column='M2ID', null=True)),
                ('vs_form', models.IntegerField(blank=True, db_column='VS_FORM', null=True)),
            ],
            options={
                'db_table': 'POLIS',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='registrhistlpu',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='registrpeople',
            options={'managed': True},
        ),
        migrations.CreateModel(
            name='MpiMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(null=True)),
                ('dt_request', models.DateTimeField(null=True)),
                ('dt_response', models.DateTimeField(null=True)),
                ('mpi_request', models.TextField(blank=True, null=True)),
                ('mpi_response', models.TextField(blank=True, null=True)),
                ('rguid', models.CharField(blank=True, max_length=36, null=True)),
                ('mpi_service', models.CharField(blank=True, max_length=36, null=True)),
                ('attach_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attach.registerattach')),
            ],
        ),
    ]