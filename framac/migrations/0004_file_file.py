# Generated by Django 3.2 on 2021-04-28 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('framac', '0003_auto_20210428_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]
