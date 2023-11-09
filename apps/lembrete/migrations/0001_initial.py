# Generated by Django 3.2.7 on 2023-11-08 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lembretes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(blank=True, null=True)),
                ('modificado_em', models.DateTimeField(blank=True, null=True)),
                ('titulo', models.CharField(max_length=255, verbose_name='Titulo')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('url_solicitada', models.CharField(max_length=500, verbose_name='URL')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Pendente'), (2, 'Visualizado'), (3, 'Cancelado'), (4, 'Finalizado')], null=True, verbose_name='Status')),
                ('prioridade', models.IntegerField(choices=[(1, 'Baixa'), (2, 'Media'), (3, 'Alta')], default=1, verbose_name='Prioridade')),
                ('lembrete_proprio', models.BooleanField(default=False, verbose_name='Lembrete próprio')),
                ('documento', models.FileField(blank=True, null=True, upload_to='lembretes')),
                ('criado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lembretes_criado_por', to=settings.AUTH_USER_MODEL)),
                ('destinatario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lembretes_destinatario', to=settings.AUTH_USER_MODEL, verbose_name='Destinatário')),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lembretes_modificado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lembrete',
                'verbose_name_plural': 'Lembretes',
            },
        ),
    ]
