# Generated by Django 4.1.6 on 2023-02-12 18:16

from django.db import migrations, models
import portfolio.models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_portfolioimage_image_alter_portfolioitem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioimage',
            name='image',
            field=models.ImageField(upload_to=portfolio.models.PortfolioImage.get_upload_path),
        ),
    ]
