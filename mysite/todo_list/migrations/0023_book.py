# Generated by Django 2.2.7 on 2019-12-25 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0022_coin_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('publication_date', models.DateField(null=True)),
                ('author', models.CharField(blank=True, max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pages', models.IntegerField(blank=True, null=True)),
                ('book_type', models.PositiveSmallIntegerField(choices=[(1, 'Hardcover'), (2, 'Paperback'), (3, 'E-book')])),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
