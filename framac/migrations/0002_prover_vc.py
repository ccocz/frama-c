# Generated by Django 3.2 on 2021-04-30 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('framac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
    ]
