# Generated by Django 2.1.2 on 2022-06-07 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220604_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['created_time']},
        ),
    ]
