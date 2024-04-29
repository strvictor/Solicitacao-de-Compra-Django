from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
            return HttpResponse(f'Email ou Senha incorretos!')
        

        
# login deu errado, redirecionando para /autenticacao/
@login_required(login_url="/autenticacao/")
def sessaopro(request):
    # login deu certo redirecionando para a pagina final
    return render(request, 'autenticado.html')
    
