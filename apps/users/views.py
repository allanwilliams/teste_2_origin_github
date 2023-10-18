from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from apps.users.forms import ImportarUsuariosForm
from apps.users.models import Papeis
from apps.django_sso_app.helpers import import_user
from datetime import datetime
import os
import csv
import re

User = get_user_model()

@login_required
@permission_required("users.add_user", raise_exception=True)
def importar_usuarios(request):
    mensagem = ''
    data = []
    fusionauth_users = []
    if request.method == "POST":
        form = ImportarUsuariosForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(arquivo.name, arquivo )
            uploaded_file_url = fs.url(filename)
            diretorio = os.path.dirname(os.path.dirname(filename))
            diretorio_arquivo = '{}{}{}'.format(settings.BASE_DIR,diretorio,uploaded_file_url)
            with open(diretorio_arquivo, encoding='utf-8') as f:
                csv_reader = csv.reader(f, delimiter=';')
                csv_reader.__next__()
                for row in csv_reader:
                    nome = row[0]
                    cpf = row[1]
                    matricula = row[2]
                    papel = row[3]
                    username = row[4]
                    email = row[5]
                    grupo = row[6]
                    staff = row[7]

                    if not matricula:
                        matricula: None
                        
                    result_data = {
                        'nome': nome,
                        'cpf': cpf,
                        'matricula': matricula,
                        'papel': papel,
                        'username': username,
                        'email': email,
                        'grupo': grupo,
                        'staff': True if staff == 'True' else False
                    }

                    cpf_clear = re.sub('[^0-9]', '', cpf)

                    usuario_multi_existe = User.objects.filter(username=username.strip()).exists()
                    email_existe = User.objects.filter(email=email.strip()).exists()
                    
                    matricula_multi_existe = False
                    if matricula:
                        matricula_multi_existe = User.objects.filter(matricula=matricula.strip()).exists()
                    
                    cpf_multi_existe = False
                    if cpf_clear:    
                        cpf_multi_existe =  User.objects.filter(cpf=cpf_clear.strip()).exists()

                    if usuario_multi_existe or cpf_multi_existe or email_existe or matricula_multi_existe:
                        result_data['status'] = 'danger'
                        result_data['status_mensagem'] = 'Não importado. Já existe um usuário cadastrado com esse username, email, cpf ou matricula'
                    else:
                        password = '{}!U'.format(cpf_clear.strip()[:7])

                        user_data = {
                            'is_superuser': False,
                            'username': username,
                            'first_name':  nome.split()[0] if len(nome.split()) > 0 else '',
                            'last_name': nome.split()[-1] if len(nome.split()) > 1 else '',
                            'email': email.strip(),
                            'is_staff': staff,
                            'is_active': True,
                            'date_joined': datetime.now(),
                            'name': nome.strip(),
                            'papel_id': papel,
                            'password': password
                        }
                        if settings.USE_FUSIONAUTH:
                            fusionauth_users.append(user_data)

                        if matricula:
                            user_data['matricula'] = matricula
                        
                        if cpf_clear:
                            user_data['cpf'] = cpf_clear


                        user = User(**user_data)

                        user.set_password(password)
                        user.save()
                        group = Group.objects.get(pk=grupo)
                        user.groups.add(group)

                    data.append(result_data)
            
            if len(fusionauth_users) > 0:
                result_import_fusion = import_user(fusionauth_users)
                if result_import_fusion:
                    for result_error in result_import_fusion:
                        for index, item in enumerate(data):
                            if item['email'] == result_error['user_email']:
                                data[index]['status'] = 'danger'
                                data[index]['status_mensagem'] = result_error['error']

            fs.delete(arquivo.name)
            mensagem = 'Upload realizado com sucesso!'
    papeis = Papeis.objects.all()
    grupos = Group.objects.all()

    context = {
        'texto': mensagem,
        'planilha': data,
        'papeis': papeis,
        'grupos': grupos,
    }

    return render(request, 'importar_usuarios.html', context)
