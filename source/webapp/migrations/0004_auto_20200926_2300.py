# Generated by Django 2.2.13 on 2020-09-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200926_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='product_pics/default.png', null=True, upload_to='product_pics', verbose_name='Картинка'),
        ),
    ]