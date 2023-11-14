from django import template
from apps.core.encrypt_url_utils import encrypt

register = template.Library()

@register.filter
def encfile(src): # pragma: no cover
    if src:
        if 'media/' not in src:
            path = src.split('/')
            name = path.pop()
            path = '/'.join(path)
            return f'{path}/{encrypt(name)}'
        else:
            arr_media = src.split('/')
            media = arr_media[1]
            arr_media.pop(0)
            arr_media.pop(0)
            
            name = arr_media.pop()
            if arr_media:
                path = '/'.join(arr_media)
                return f'/{media}/{path}/{encrypt(name)}'
        
@register.filter
def dd(src): # pragma: no cover
    return dir(src)