# Generated by Django 3.2.7 on 2023-09-29 17:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Nome Completo')),
                ('matricula', models.CharField(blank=True, help_text='Obrigatório para cadastro de defensores', max_length=11, null=True, unique=True, verbose_name='Matricula')),
                ('num_orgao_classe', models.CharField(blank=True, max_length=255, null=True, verbose_name='Número do Órgão de Classe')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF')),
                ('sexo', models.IntegerField(choices=[(0, 'Não informado'), (1, 'Masculino'), (2, 'Feminino')], default=0, verbose_name='Sexo')),
                ('user_str', models.CharField(blank=True, max_length=200, null=True, verbose_name='User String')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Defensores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(blank=True, null=True)),
                ('modificado_em', models.DateTimeField(blank=True, null=True)),
                ('nome', models.CharField(max_length=150, verbose_name='Nome')),
                ('matricula', models.CharField(max_length=11, verbose_name='Matricula')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('criado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='defensores_criado_por', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='defensores_modificado_por', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='defensores_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Defensores',
                'verbose_name_plural': 'Defensores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Papeis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(blank=True, null=True)),
                ('modificado_em', models.DateTimeField(blank=True, null=True)),
                ('titulo', models.CharField(max_length=25, verbose_name='Título')),
                ('criado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='papeis_criado_por', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='papeis_modificado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Papel',
                'verbose_name_plural': 'Papeis',
                'ordering': ['titulo'],
            },
        ),
        migrations.CreateModel(
            name='DefensoresLotacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(blank=True, null=True)),
                ('modificado_em', models.DateTimeField(blank=True, null=True)),
                ('defensor_nome', models.CharField(max_length=255, verbose_name='Defensor')),
                ('defensor_matricula', models.CharField(db_index=True, max_length=11, verbose_name='Matricula')),
                ('defensor_cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('defensor_email', models.CharField(max_length=255, null=True, verbose_name='E-mail')),
                ('defensoria', models.CharField(max_length=255, verbose_name='Defensoria')),
                ('tipo', models.CharField(max_length=50, verbose_name='Tipo')),
                ('titularidade_designacao', models.CharField(max_length=50, verbose_name='Titularidade ou Designação')),
                ('origem', models.CharField(max_length=255, verbose_name='Origem')),
                ('origem_id', models.IntegerField(verbose_name='Identificador da Origem')),
                ('data_inicio', models.DateField(db_index=True, verbose_name='Data de Início')),
                ('data_termino', models.DateField(blank=True, db_index=True, null=True, verbose_name='Data de Término')),
                ('nucleo_txt', models.CharField(blank=True, max_length=255, null=True, verbose_name='Núcleo')),
                ('defensoreslocacoes_str', models.CharField(blank=True, max_length=255, null=True, verbose_name='Defensor(a)/Defensoria')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Está ativa?')),
                ('criado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='defensoreslotacoes_criado_por', to=settings.AUTH_USER_MODEL)),
                ('defensor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='defensoreslotacoes_defensores', to='users.defensores', verbose_name='Defensor')),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='defensoreslotacoes_modificado_por', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='defensoreslotacoes_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lotação dos defensores',
                'verbose_name_plural': 'Lotações dos defensores',
                'ordering': ['-data_inicio'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='papel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_papel', to='users.papeis', verbose_name='Papeis'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
