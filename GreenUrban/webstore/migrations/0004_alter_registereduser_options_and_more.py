# Generated by Django 5.0.6 on 2024-07-11 05:30

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0003_alter_registereduser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registereduser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='number',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='pincode',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
