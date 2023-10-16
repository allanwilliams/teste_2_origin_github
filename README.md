![Alt text](/static/logo-vertical-novo-modelo.png)
# Template Django Admin
Supported by✨COTIN✨

Esse é um template base para criação de novos projetos baseados em Django Admin. Após clonar o repositório a pasta .git deverá ser deletada antes de inciar o desenvolvimento.
## Tecnologias

- [Django](https://www.djangoproject.com/) - Verison 3.2.7
- [Python](https://www.python.org/) - version 3.8.*



## Instalação
Instale o Virtualenv, certifique-se de estar dentro da pasta do projeto ...
```sh
 cd pasta-do-projeto
 ```

Crie a Virtualenv ...
```sh
python -m venv venv
source venv/bin/activate
```

Instale as dependências da venv ...
```sh
pip install -r requirements.txt
```

Configurando a .env
```sh
cp .env_exemplo .env
```

## Integração com FusionAuth

Caso deseje utilizar o FusionAuth os parametros abaixo deverão ser configurados na .env
```
[FUSIONAUTH_HOST]: Endereço do servidor do FusionAuth ex: http://127.0.0.1:9011/
[USE_FUSIONAUTH]: Flag que habilita a integração (se for False a autenticação será feita usando Django Admin convencional)
[FUSIONAUTH_USER_API_KEY]: Chave de segurança para a API de User do FusionAuth
[OIDC_RP_CLIENT_ID]: ID gerado para a aplicação no FusionAuth
[OIDC_RP_CLIENT_SECRET]: SECRET gerado para a aplicação no FusionAuth
```

## Padrões de Roles FusionAuth
Sempre que uma nova application for inicializada no FusionAuth as roles de controle deverão ser criadas
```
FLAG[IS_ADMIN]: Garante acesso administrativo ao usuário dentro do ambiente da aplicação
FLAG[IS_STAFF]: Garante acesso ao usuário dentro do ambiente da aplicação
```

- Configuração de Papeis

As roles de papel deverão possuir a palavra chave PAPEL(caixa alta) e o nome do papel dentro de [] (cochetes). Dessa forma o django_sso_app irá reconhecer o papel do usuário e atualiza-lo corretamente. 
Obs: Somente uma role de Papel poderá ser habilitada por usuário na Aplicação, caso mais de uma seja habilitada a ultima role é que valerá.

exemplo:
```
PAPEL[Colaborador(a)]
```

- Configurações de Grupos

As roles de grupo deverão possuir a palavra chave GRUPO(caixa alta) e o nome do grupo dentro de [] (cochetes)

exemplo:
```
GRUPO[Defensores]
```

## Testes
Antes de iniciar os testes habilite a venv
```
source venv/bin/activate
```
Executando todos dos testes

```
coverage run manage.py test apps; coverage html --omit="*/venv/*,config/*,static/*,staticfiles/*,adminlteui/*" -d tests/coverage
```

Executando testes por app

```
coverage run manage.py test apps/{nome_do_app}; coverage html --omit="*/venv/*,config/*,static/*,staticfiles/*,adminlteui/*" -d tests/coverage
```

Os resultados dos testes serão gravados na pasta tests/coverage/ e podem ser acessados abrindo o arquivo tests/coverage/index.html