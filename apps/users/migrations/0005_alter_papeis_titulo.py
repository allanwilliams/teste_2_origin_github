# Generated by Django 3.2.7 on 2023-10-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_cpf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papeis',
            name='titulo',
            field=models.CharField(max_length=500, verbose_name='Título'),
        ),
    ]
