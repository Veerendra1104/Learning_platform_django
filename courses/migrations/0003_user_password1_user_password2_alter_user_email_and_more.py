# Generated by Django 5.1 on 2024-09-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_user_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password1',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
