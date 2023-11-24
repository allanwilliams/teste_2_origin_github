# Generated by Django 3.2.7 on 2023-11-16 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20231110_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferencias',
            name='preferencia',
            field=models.IntegerField(choices=[(1, 'Menu fixo')], verbose_name='Preferência'),
        ),
        migrations.CreateModel(
            name='CredenciaisUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(blank=True, null=True)),
                ('modificado_em', models.DateTimeField(blank=True, null=True)),
                ('sistema', models.IntegerField(choices=[(1, 'PJE'), (2, 'ESAJ'), (3, 'SEEU')], verbose_name='Sistema')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('criado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='credenciaisusuario_criado_por', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='credenciaisusuario_modificado_por', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='credenciaisusuario_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]