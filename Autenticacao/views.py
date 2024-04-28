from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse

def autenticacao(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Autenticar usando o email
        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
            # Autenticação bem-sucedida
            login(request, usuario)

            return HttpResponse(f'Deu Certo!!')
        else:
            # Autenticação falhou
            return HttpResponse(f'Deu errado!!')



def sessao_pro(request):
    return HttpResponse("Sessão Pro")
