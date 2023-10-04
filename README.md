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

Caso deseje utilizar o FusionAuth os parametros abaixo deverãos ser configurados na .env
```
[FUSIONAUTH_HOST]: Endereço do servidor do FusionAuth ex: http://127.0.0.1:9011/
[USE_FUSIONAUTH]: Flag que habilita a integração (se for False a autenticação será feita usando Django Admin convencional)
[FUSIONAUTH_USER_API_KEY]: Chave de segurança para a API de User do FusionAuth
[OIDC_RP_CLIENT_ID]: ID gerado para a aplicação no FusionAuth
[OIDC_RP_CLIENT_SECRET]: SECRET gerado para a aplicação no FusionAuth
```
