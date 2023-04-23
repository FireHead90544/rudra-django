# Generated by Django 4.1.6 on 2023-03-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitehome', '0004_alter_timelineitem_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('message', models.TextField(max_length=2000)),
                ('score', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]