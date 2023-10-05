from .models import LogRequests, UserPage
import json
from .models import UserSession
from threading import Thread
from asgiref.sync import sync_to_async
import asyncio
import datetime
from django.db.utils import InterfaceError
from django.shortcuts import redirect
from apps.users.models import UserPreferencias

block_list = [
    '/core/api/general/',
    '/lembrete/api/lembretes/',
    '/admin/jsi18n/',
    '/favicon.ico',
    '/resources/',
    '/app-assistido/api/user',
    '/admin/jsi',
    '/ajax_select/ajax_lookup',
    '/atendimento/api/',
    '/api/',
    '/__debug__/history_sidebar/'
]
class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            req = request
            if not req.user.is_authenticated and '/admin/' in request.META['PATH_INFO'] and '/admin/login' not in request.META['PATH_INFO']:
                return redirect('/admin/login')
            
            if self.valida_url(request.META['PATH_INFO']):
                Thread(target=self.main,args=(req,)).run()
            return self.get_response(req)
        except InterfaceError as e:
            asyncio.run(self.close_connection())
            return self.get_response(req)

    def valida_url(self,url):
        if '/core/api/general/session/UserPage/' in url:
            return True
        
        for bl in block_list:
            if bl in url:
                return False
        return True

    def main(self,request):
        grava_log = True
        if '/core/api/general/session/UserPage/' in request.META['PATH_INFO']:
            grava_log = False
        req = request
        autenticado = asyncio.run(self.get_autenticado(req))
        params = req.POST if req.POST else req.GET

        dic_logrequest = {
            'ip': req.META['REMOTE_ADDR'],
            'ip_publico': req.META.get('HTTP_X_REAL_IP') or None,
            'navegador': req.META['HTTP_USER_AGENT'],
            'url_atual': req.META.get('HTTP_REFERER') or None,
            'url': req.META['PATH_INFO'],
            'metodo': req.method,
            'parametros': json.dumps(params,ensure_ascii=False)
        }

        if autenticado and grava_log:
            if 'sessionid' in req.COOKIES:
                dic_logrequest.update({'session_key':req.COOKIES['sessionid']})
                dic_logrequest.update({'user':req.user})
                asyncio.run(self.get_usersession(req))

                asyncio.run(self.save_logrequests(dic_logrequest))
                asyncio.run(self.verifica_preferencia(request))
        staff = asyncio.run(self.is_staff(req))
        if staff:
            url = ''
            try:
                if req.META.get('HTTP_REFERER'):
                    if '/admin/' in req.META.get('HTTP_REFERER'):
                        url = '/admin/' + req.META.get('HTTP_REFERER').split('/admin/')[1]
                    else:
                        url = req.META['PATH_INFO']
                else:
                    url = req.META['PATH_INFO']
            except:
                url = req.META['PATH_INFO']
                
            asyncio.run(self.save_userpage(req,url))     

    @sync_to_async
    def save_userpage(self,request,url):
        try:
            user_page, created = UserPage.objects.get_or_create(user = request.user,url=url)
            if user_page:
                user_page.save()
        except:
            UserPage.objects.filter(user = request.user,url=url).delete()
            user_page, created = UserPage.objects.get_or_create(user = request.user,url=url)
        if user_page:
            user_page.modificado_em = datetime.datetime.now()
            user_page.save()
                
    
    async def is_staff(self,request):
        return request.user.is_staff
    
    @sync_to_async
    def save_logrequests(self,dic_logrequest):
        session = LogRequests(**dic_logrequest)
        session.save()

    @sync_to_async
    def get_autenticado(self,request):
        return request.user.is_authenticated

    @sync_to_async
    def get_usersession(self,request):
        user_session = UserSession.objects.filter(user = request.user.id).first()
        if user_session:
            user_session.modificado_em = datetime.datetime.now()
            user_session.save()
        return user_session
    
    @sync_to_async
    def close_connection(self):
        from django.db import connections, connection
        connection.close()

    @sync_to_async
    def verifica_preferencia(self, request):
        if request.user:
            try:
                preferencia = UserPreferencias.objects.filter(user=request.user, preferencia=2).first()
                if preferencia and preferencia.criado_em:
                    hoje = datetime.date.today()
                    data_preferencia = preferencia.criado_em.date()
                    if hoje > data_preferencia:
                        preferencia.delete()
            except Exception:
                pass