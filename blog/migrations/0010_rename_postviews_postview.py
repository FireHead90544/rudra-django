# Generated by Django 4.1.6 on 2023-03-07 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_postviews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostViews',
            new_name='PostView',
        ),
    ]
