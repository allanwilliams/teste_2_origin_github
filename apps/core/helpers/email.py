from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def gerar_email(subject, html_content, from_email, to):
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def gerar_email_with_files(subject, html_content, from_email, to, path = None):
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    if path:
        msg.attach(path.name, path.read(),path.content_type)
    msg.attach_alternative(html_content, "text/html")
    msg.send()    

def gerar_email_atividade_cumulativa(subject, html_content, from_email, to):
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def gerar_email_atividade_extraordinaria(subject, html_content, from_email, to):
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def gerar_email_sistema_plantao(subject, html_content, from_email, to):
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

