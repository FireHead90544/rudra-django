# Generated by Django 4.1.7 on 2023-04-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_portfolioitem_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioimage',
            name='alt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]