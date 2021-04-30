# Generated by Django 3.2 on 2021-04-29 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=400)),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('owner', models.CharField(max_length=200)),
                ('is_available', models.BooleanField(default=True)),
                ('parent_directory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='framac.directory')),
            ],
        ),
        migrations.CreateModel(
            name='SectionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SectionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('login', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StatusData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(max_length=500)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='framac.user')),
            ],
        ),
        migrations.CreateModel(
            name='FileSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=400)),
                ('creation_date', models.DateTimeField()),
                ('section_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='framac.sectioncategory')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='framac.sectionstatus')),
                ('status_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='framac.statusdata')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=400)),
                ('creation_date', models.DateTimeField()),
                ('owner', models.CharField(max_length=200)),
                ('is_available', models.BooleanField(default=True)),
                ('file', models.FileField(upload_to='framac/files')),
                ('file_sections', models.ManyToManyField(to='framac.FileSection')),
                ('parent_directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='framac.directory')),
            ],
        ),
    ]
