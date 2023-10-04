from django.shortcuts import render, redirect
from django.contrib import messages
from apps.django_sso_app.forms import AdminPasswordChangeForm

def change_password(request):
    form = AdminPasswordChangeForm(request.user)
    
    if request.method == 'POST':
        form = AdminPasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha atualizada com sucesso')
            return redirect(f'/admin/')

    context = {
        'form': form
    }

    return render(request,'django_sso_app/sso_change_password.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect(f'/admin/')
    return redirect('oidc_authentication_init')