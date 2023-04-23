# Generated by Django 4.1.6 on 2023-02-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='tldr',
            field=models.CharField(default='In this post, we will be learning about how we can integrate froala which is a what-you-see-is-what-you-get text editor which you can use as a text input editor with your django blog post.', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
