# Generated by Django 5.2.3 on 2025-06-25 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermodels',
            name='password',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customermodels',
            name='image',
            field=models.ImageField(upload_to='media/userimage'),
        ),
    ]
