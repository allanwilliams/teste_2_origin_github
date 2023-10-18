from django.conf import settings
from apps.users.models import Papeis
import requests

def import_user(users):
    errors_update = []
    for user in users:
        roles = ['FLAG[IS_STAFF]']
        papel_id = user.get('papel_id')
        if papel_id:
            papel = Papeis.objects.filter(id=papel_id).first()
            if papel:
                roles = ['FLAG[IS_STAFF]',f'PAPEL[{papel.titulo}]']
                
        new_user = {
            'active': True,
            'email': user.get('email'),
            'fullName': user.get('name'),
            'firstName': user.get('first_name'),
            'lastName': user.get('last_name'),
            'password': user.get('password'),
            'username': user.get('username'),
            'registrations': [
                {
                'applicationId': settings.OIDC_RP_CLIENT_ID,
                'roles': roles,
                'verified': True
                }
            ],
            'verified': True,
        }

        api_url = settings.FUSIONAUTH_HOST + '/api/user'
        data_user = {
            'user': new_user,
            'validateDbConstraints': True
        }

        headers = { 'Content-Type': 'application/json', 'Authorization': settings.FUSIONAUTH_USER_API_KEY }
        response = requests.post(url=api_url,json=data_user,headers=headers)

        if response.status_code != 200:
            errors = response.json()
            erro_update = handle_import_users_errors(errors,new_user)
            if erro_update:
                errors_update.append(erro_update)
        
        if response.status_code == 200:
            user_data = response.json()
            result_update = update_user(new_user,user_data)
            if result_update:
                errors_update.append({
                    'user_email': new_user['email'],
                    'error': result_update
                })
    return errors_update

def update_user(user_to_update,user_data):
    user_id = user_data['user']['id']
    registration = user_to_update.get('registrations')[0]


    api_url = settings.FUSIONAUTH_HOST + f'/api/user/registration/{user_id}'
    data_user = {
        'registration': registration,
    }

    headers = { 'Content-Type': 'application/json', 'Authorization': settings.FUSIONAUTH_USER_API_KEY }
    response = requests.post(url=api_url,json=data_user,headers=headers)

    if response.status_code != 200:
        data = response.json()
        return handle_update_users_errors(data)
    
    return False
        

def search_user(user_email):
    api_url = settings.FUSIONAUTH_HOST + f'/api/user?email={user_email}'

    headers = { 'Content-Type': 'application/json', 'Authorization': settings.FUSIONAUTH_USER_API_KEY }
    response = requests.get(url=api_url,headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    if response.status_code != 200:
        data = response.json()
        return False
    
def handle_import_users_errors(data_errors,new_user):
    for erros_type in data_errors:
        if erros_type == 'fieldErrors':
            errors = data_errors.get(erros_type)
            for error in errors:
                messages = errors.get(error)
                for message in messages:
                    if message.get('code') == '[duplicate]user.email':
                        user_data = search_user(new_user['email'])
                        result_update = update_user(new_user,user_data)
                        if result_update:
                            return {
                                'user_email': new_user['email'],
                                'error': result_update
                            }
                            
    

def handle_update_users_errors(data_errors):
    for erros_type in data_errors:
        if erros_type == 'fieldErrors':
            errors = data_errors.get(erros_type)
            for error in errors:
                messages = errors.get(error)
                for message in messages:
                    if message.get('code') == '[duplicate]registration':
                        return 'Usuário já registrado no FusionAuth e pode acessar normalmente!'