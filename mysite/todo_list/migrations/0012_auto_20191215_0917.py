# Generated by Django 2.2.7 on 2019-12-15 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0011_auto_20191215_0909'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.AlterModelTable(
            name='category',
            table='CATEGORIES',
        ),
    ]
