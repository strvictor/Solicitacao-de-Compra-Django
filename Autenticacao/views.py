from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
            return redirect('home')
        else:
            # Autenticação falhou
            return render(request, 'login.html', {'login_errado': 'E-mail ou Senha incorretos!'})
        

# login deu errado, redirecionando para /autenticacao/
@login_required(login_url="/autenticacao/")
def home(request):
    # login deu certo redirecionando para a pagina final
    return render(request, 'autenticado.html')








usuario1 = User.objects.get(email='vicctor1009@gmail.com')

grupos_do_usuario = usuario1.groups.all()

if len(grupos_do_usuario) == 1 and grupos_do_usuario:
    print(grupos_do_usuario[0])

else:
    for grupo in grupos_do_usuario:
        print("Grupo:", grupo)