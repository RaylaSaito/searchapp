# Generated by Django 5.1.3 on 2024-11-14 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]