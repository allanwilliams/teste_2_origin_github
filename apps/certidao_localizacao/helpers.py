import hashlib
import os
from .models import Certidao

def get_hash():
    return hashlib.md5(os.urandom(128)).hexdigest().upper()[:16]

def url_img_token(token): # pragma: no cover
    url = '{0}?token={1}'.format(base_url('certidao_localizacao/verificar-assinatura'), token)
    return qrcode(url, '96x96')

def url_verificador(): # pragma: no cover
    return base_url('certidao_localizacao/verificar-assinatura')

def qrcode(value, size="128x128"):
    return "https://chart.apis.google.com/chart?cht=qr&chs={0}&chl={1}&chld=L|0".format(size, value)

def base_url(value):
    # protocolo = 'http' if config.DOMINIO_ATUAL == 'localhost:8000' else 'https'
    # return "{0}://{1}/{2}".format(protocolo, config.DOMINIO_ATUAL, value)
    return f"http://localhost:8000/{value}"

def url_img_mobile(user):
    certidao = Certidao.objects.filter(criado_por=user,assinatura = False).first()
    if not certidao:
        certidao = Certidao.objects.create()
        
    url = '{0}?certidao={1}'.format(base_url('certidao_localizacao/assinar-certidao'),certidao.get_encrypt_id())
    return {
        'img':qrcode(url, '300x300'),
        'certidao_id': certidao.id
    }