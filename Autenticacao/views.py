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
            login(request, usuario)
            # usuario ja autenticado
            return render(request, 'autenticado.html')
        else:
            # Autenticação falhou
            return HttpResponse(f'Deu errado!!')


def sessaopro(request):
    if request.user.is_authenticated:
        # usuario está autenticado e estou redirecionando para a pagina autenticado.html
        return render(request, 'autenticado.html')
    
    else:
        # não esta autenticado e precisa fazer o login
        return render(request, 'login.html')
