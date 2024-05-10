from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Pedido.models import Dados
from Pedido.models import UsuariosBD
from django.core.paginator import Paginator
from django.http import HttpResponse
from .motivacao import APIConselhos
import datetime


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

    nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)
    print(f'SETOR:', setor)
    # pega tudo
    #dados = Dados.objects.all()

    if str(permissao_usuario) == "Coodernador":
        estagio_update = "1/5"
    elif str(permissao_usuario) == "Gerente":
        estagio_update = "2/5"
    elif str(permissao_usuario) == "Analista de Compras":
        estagio_update = "3/5"
    elif str(permissao_usuario) == "Diretor Financeiro":
        estagio_update = "4/5"


    if setor == None:
        # se cair aqui é pq não é coodernador
        dados = Dados.objects.filter(estagio=estagio_update)
    else:
        # pega com base na permisao do usuario | é coodernador
        dados = Dados.objects.filter(estagio=estagio_update, setor=setor)

    mensagem = ''
    if len(dados) == 0:
        mensagem = 'Sem novas solicitações.'

    #adicionando a paginacao
    dados_paginacao = Paginator(dados, 5)
    pagina_numero = request.GET.get('page')
    pagina = dados_paginacao.get_page(pagina_numero)

    return render(request, 'autenticado.html', {"pagina": pagina,
                                                "nome_usuario": nome_completo,
                                                "saudacao": saudacao(),
                                                "concelho": api_concelho(),
                                                "mensagem": mensagem
                                                })

def retorna_dados_usuario(request):
    usuario_autenticado = request.user

    # Acessando nome e email do usuário autenticado
    nome_inicio = usuario_autenticado.first_name
    nome_final = usuario_autenticado.last_name
    nome_completo = nome_inicio + ' ' + nome_final
    email = usuario_autenticado.email

    usuario1 = User.objects.get(email=email)
    grupos_do_usuario = usuario1.groups.all()

    if len(grupos_do_usuario) == 1 and grupos_do_usuario:
        grupo_final_usuario = grupos_do_usuario[0]
    else:
        grupo_final_usuario = 'usuario tem mais de 1 grupo, favor tratar!'

    # pega o setor do usuario com base em seu nome
    captura_setor =  UsuariosBD.objects.filter(nome=nome_completo).first()
    if captura_setor:
        setor = captura_setor.setor
    else:
        setor = None

    return nome_completo, grupo_final_usuario, setor


def saudacao():
    hora_atual = datetime.datetime.now().hour
    
    if 6 <= hora_atual < 12:
        return "Bom dia"
    elif 12 <= hora_atual < 18:
        return "Boa tarde"
    else:
        return "Boa noite"


def api_concelho():
    api = APIConselhos()
    conselho = api.obter_conselho_aleatorio()
    if conselho:
        return conselho


def aprovar_dado(request):
    if request.method == 'POST':
        id_linha = request.POST.get('dado_id')

        nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)

        if str(permissao_usuario) == "Coodernador":
            estagio_update = "2/5"
        elif str(permissao_usuario) == "Gerente":
            estagio_update = "3/5"
        elif str(permissao_usuario) == "Analista de Compras":
            estagio_update = "4/5"
        elif str(permissao_usuario) == "Diretor Financeiro":
            estagio_update = "5/5"
        else:
            estagio_update = 'nenhum!!!!!!!!'

        # Obtém o objeto do modelo que você deseja modificar
        objeto = Dados.objects.get(pk=id_linha)

        # Modifica os atributos do objeto
        objeto.status = "Aprovado"
        objeto.estagio = estagio_update
        objeto.ultima_atualizacao = nome_completo
        objeto.save()  # Salva as alterações no banco de dados

        return redirect('home')
    else:
        return redirect('home')


def reprovar_dado(request):
    if request.method == 'POST':
        id_linha = request.POST.get('dado_id')
        
        return HttpResponse(f'Dado reprovado com sucesso. {id_linha}')
    else:
        return redirect('home')


def pedidos_aprovados(request):

    nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)
    print(f'SETOR:', setor)

    # pega tudo
    #dados = Dados.objects.all()

    if setor == None:
        # entra aqui se não é coodernador, ou seja, pega os gerentes, analistas, diretor... retorno do banco todos os dados que estiverem do estagio 2/5 >, ou seja ja passou por ele

        if str(permissao_usuario) == 'Gerente':
            estagio = ['2/5', '3/5', '4/5', '5/5']
            permitidos = ['Aline Araujo', 'Giovane Lobato', 'Gerlem Brito']

        elif str(permissao_usuario) == 'Analista de Compras':
            estagio = ['3/5', '4/5', '5/5']
            permitidos = ['Giovane Lobato', 'Gerlem Brito']

        elif str(permissao_usuario) == 'Diretor Financeiro':
            estagio = ['5/5'] # retirei o 4/5
            permitidos = ['Gerlem Brito']
        else:
            print('erro aqui brow')


        print(permissao_usuario)
        print(estagio)
        dados = Dados.objects.filter(estagio__in=estagio, status='Aprovado', ultima_atualizacao__in=permitidos)

    else:
        dados = Dados.objects.filter(setor=setor, status='Aprovado')

    mensagem = ''
    if len(dados) == 0:
        mensagem = 'Sem novas solicitações.'

    dados_com_indices = [(index + 1, dado) for index, dado in enumerate(dados)]

   #adicionando a paginacao
    dados_paginacao = Paginator(dados_com_indices, 1)
    pagina_numero = request.GET.get('page')
    pagina = dados_paginacao.get_page(pagina_numero)

    return render(request, 'pedidos_aprovados.html', {"pagina": pagina,
                                                "nome_usuario": nome_completo,
                                                "saudacao": saudacao(),
                                                "concelho": api_concelho(),
                                                "mensagem": mensagem})
