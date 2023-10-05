# Generated by Django 2.2.2 on 2022-11-01 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('session', '0003_logrequests_ip_publico'),
    ]

    operations = [
        migrations.AddField(
            model_name='logrequests',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='logrequests',
            name='url_atual',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='logrequests',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='logrequests_usersession', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.CreateModel(
            name='UserPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(blank=True, null=True)),
                ('modificado_em', models.DateTimeField(blank=True, null=True)),
                ('url', models.CharField(max_length=500, verbose_name='url')),
                ('criado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userpage_criado_por', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userpage_modificado_por', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'usuário página',
                'verbose_name_plural': 'Usuários página',
            },
        ),
    ]
