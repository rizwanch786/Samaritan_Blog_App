# Generated by Django 3.2.8 on 2021-10-11 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20211011_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='parent',
        ),
    ]
