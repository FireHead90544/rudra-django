# Generated by Django 4.1.1 on 2022-09-20 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitehome', '0002_rename_classes_mysociallink_fa_classes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimelineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
