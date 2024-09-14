from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from Pedido.models import UsuariosBD
from .motivacao import APIConselhos
from django.conf import settings
from Pedido.models import Dados
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
            return redirect('pedidos_pendentes')
        else:
            # Autenticação falhou
            return render(request, 'login.html', {'login_errado': 'E-mail ou Senha incorretos!'})
        
        
# login deu errado, redirecionando para /autenticacao/
@login_required(login_url="/autenticacao/")
def pedidos_pendentes(request):

    nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)
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


    if setor == 'None':
        # se cair aqui é pq não é coodernador
        print('to aquiddddd')
        dados = Dados.objects.filter(estagio=estagio_update, status='Aprovado')
    else:
        # pega com base na permisao do usuario | é coodernador
        print('é aqui q to')
        dados = Dados.objects.filter(estagio=estagio_update, setor=setor, status='Pendente')

    mensagem = ''
    if len(dados) == 0:
        mensagem = 'Sem novas solicitações.'

    dados_com_indices = [(index + 1, dado) for index, dado in enumerate(dados)]
    #adicionando a paginacao
    dados_paginacao = Paginator(dados_com_indices, 5)
    pagina_numero = request.GET.get('page')
    pagina = dados_paginacao.get_page(pagina_numero)

    return render(request, 'autenticado.html', {"pagina": pagina,
                                                "nome_usuario": nome_completo,
                                                "saudacao": saudacao(),
                                                "concelho": api_concelho(),
                                                "mensagem": mensagem,
                                                'permissao_usuario': str(permissao_usuario),
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
        print(grupo_final_usuario)
    else:
        grupo_final_usuario = 'usuario tem mais de 1 grupo, favor tratar!'

    # pega o setor do usuario com base em seu nome
    captura_setor =  UsuariosBD.objects.filter(nome=nome_completo).first()
    if captura_setor == 'None':
        setor = 'None'
    else:
        setor = captura_setor.setor
        print(setor)
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
    # api = APIConselhos()
    # conselho = api.obter_conselho_aleatorio()
    # if conselho:
    #   return conselho
    return ''


@login_required(login_url="/autenticacao/")
def aprovar_dado(request):
    if request.method == 'POST':
        id_linha = request.POST.get('dado_id')

        if 'arquivo' in request.FILES:
            # cotação do analista de compras
            arquivo = request.FILES['arquivo']

        else:
            arquivo = ''

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

        setor_do_pedido_atual = objeto.setor

        # Modifica os atributos do objeto
        objeto.status = "Aprovado"
        objeto.estagio = estagio_update
        objeto.ultima_atualizacao = nome_completo
        objeto.arquivo = arquivo
        objeto.save()  # Salva as alterações no banco de dados

        # estou capturando o estagio dos staffs pra envio de email informando nova solicitação!
        if estagio_update == '5/5':
            # seria a prroxima pessoa que o diretor financeiro envia mensagem, pode ser a suellem
            pass
        else:
            captura_estagio =  UsuariosBD.objects.filter(estagio=estagio_update).first()
            nome = captura_estagio.nome
            email = captura_estagio.email

            enviar_email(request, nome, email, setor_do_pedido_atual, "Aprovado")
            
            
            
            
            
            email_solicitante = objeto.email
            nome_solicitante = objeto.nome
            
            enviar_email_usuario(nome_solicitante, email_solicitante, setor_do_pedido_atual, "Aprovado")
            
            print(f'quem solicitou o pedido tem o email {email_solicitante}')
            
            
            
            
            

        return redirect('pedidos_pendentes')
    else:
        return redirect('pedidos_pendentes')


@login_required(login_url="/autenticacao/")
def reprovar_dado(request):
    if request.method == 'POST':
        id_linha = request.POST.get('dado_id')

        nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)

        if str(permissao_usuario) == "Coodernador":
            estagio_update = "1/5"
        elif str(permissao_usuario) == "Gerente":
            estagio_update = "2/5"
            permitidos = ['1/5']
        elif str(permissao_usuario) == "Analista de Compras":
            estagio_update = "3/5"
            permitidos = ['1/5', '2/5']
        elif str(permissao_usuario) == "Diretor Financeiro":
            estagio_update = "4/5"
            permitidos = ['1/5', '2/5', '3/5']
        else:
            estagio_update = 'nenhum!!!!!!!!'

        # Obtém o objeto do modelo que você deseja modificar
        objeto = Dados.objects.get(pk=id_linha)

        setor_do_pedido_atual = objeto.setor

        # Modifica os atributos do objeto
        objeto.status = "Reprovado"
        objeto.estagio = estagio_update
        objeto.ultima_atualizacao = nome_completo
        objeto.save()  # Salva as alterações no banco de dados

        # estou capturando o estagio dos staffs pra envio de email informando nova solicitação!
        if estagio_update == '0/5':
            pass
        else:
            captura_estagio =  UsuariosBD.objects.filter(estagio__in=permitidos)

            for usuario in captura_estagio:
                nome = usuario.nome
                email = usuario.email
                setor_usuario = usuario.setor

                if str(setor_do_pedido_atual) == str(setor_usuario) or setor_usuario == 'None':
                    print(nome, email)
                    enviar_email(request, nome, email, setor_do_pedido_atual, "Reprovado")
                    
                    
                    
                    email_solicitante = objeto.email
                    nome_solicitante = objeto.nome
                    
                    enviar_email_usuario(nome_solicitante, email_solicitante, setor_do_pedido_atual, "Reprovado")
                    
                    
                    
                    
                else:
                    print('setor errado:', nome, email, setor_usuario)

        return redirect('pedidos_pendentes')
    else:
        return redirect('pedidos_pendentes')
    
    
@login_required(login_url="/autenticacao/")
def pedidos_aprovados(request):

    nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)
    print(f'SETOR:', setor)

    # pega tudo
    #dados = Dados.objects.all()

    if setor == 'None':
        # entra aqui se não é coodernador, ou seja, pega os gerentes, analistas, diretor... retorno do banco todos os dados que estiverem do estagio 2/5 >, ou seja ja passou por ele

        if str(permissao_usuario) == 'Gerente':
            estagio = ['2/5', '3/5', '4/5', '5/5']
            permitidos = ['Aline Araujo', 'Giovane Lobato', 'Gerlem Brito', 'Usuario Gerente']

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
    dados_paginacao = Paginator(dados_com_indices, 5)
    pagina_numero = request.GET.get('page')
    pagina = dados_paginacao.get_page(pagina_numero)

    return render(request, 'pedidos_aprovados.html', {"pagina": pagina,
                                                "nome_usuario": nome_completo,
                                                "saudacao": saudacao(),
                                                "concelho": api_concelho(),
                                                "mensagem": mensagem})


@login_required(login_url="/autenticacao/")
def pedidos_reprovados(request):

    nome_completo, permissao_usuario, setor = retorna_dados_usuario(request)
    print(f'SETOR:', setor)

    # pega tudo
    #dados = Dados.objects.all()

    if setor == 'None':
        # entra aqui se não é coodernador, ou seja, pega os gerentes, analistas, diretor... retorno do banco todos os dados que estiverem do estagio 2/5 >, ou seja ja passou por ele

        if str(permissao_usuario) == 'Gerente':
            estagio = ['2/5', '3/5', '4/5', '5/5']
            permitidos = ['Aline Araujo', 'Giovane Lobato', 'Gerlem Brito', 'Usuario Gerente']

        elif str(permissao_usuario) == 'Analista de Compras':
            estagio = ['3/5', '4/5', '5/5']
            permitidos = ['Giovane Lobato', 'Gerlem Brito']

        elif str(permissao_usuario) == 'Diretor Financeiro':
            estagio = ['4/5'] # retirei o 4/5
            permitidos = ['Gerlem Brito']
        else:
            print('erro aqui brow')


        print(permissao_usuario)
        print(estagio)
        dados = Dados.objects.filter(estagio__in=estagio, status='Reprovado', ultima_atualizacao__in=permitidos)

    else:
        dados = Dados.objects.filter(setor=setor, status='Reprovado')

    mensagem = ''
    if len(dados) == 0:
        mensagem = 'Sem novas solicitações.'

    dados_com_indices = [(index + 1, dado) for index, dado in enumerate(dados)]

   #adicionando a paginacao
    dados_paginacao = Paginator(dados_com_indices, 5)
    pagina_numero = request.GET.get('page')
    pagina = dados_paginacao.get_page(pagina_numero)

    return render(request, 'pedidos_reprovados.html', {"pagina": pagina,
                                                "nome_usuario": nome_completo,
                                                "saudacao": saudacao(),
                                                "concelho": api_concelho(),
                                                "mensagem": mensagem})


def enviar_email(request, nome_usuario, email_usuario, setor_usuario, tipo_mensagem):
    
    # Renderiza o modelo HTML como uma string
    html_content = render_to_string('email_templates/email_template.html',
                                    {'nome': nome_usuario,
                                     'setor': setor_usuario,
                                     'tipo_mensagem': tipo_mensagem,
                                     })
    
    # Converte o HTML para texto sem formatação
    text_content = strip_tags(html_content)

    if tipo_mensagem == 'Aprovado':
        mensagem = 'Nova Solicitação de Compra | Cabana Clube'
    else:
        mensagem = 'Solicitação de Compra Reprovada | Cabana Clube'

    # Cria o e-mail
    email = EmailMultiAlternatives(
        mensagem,  # Assunto
        text_content,  # Corpo do e-mail em texto sem formatação
        settings.EMAIL_HOST_USER,  # Remetente
        [email_usuario]  # Lista de destinatários
    )
    
    # Adiciona o conteúdo HTML ao e-mail
    email.attach_alternative(html_content, "text/html")
    
    # Envia o e-mail
    email.send()
    
    
    
    
    
def enviar_email_usuario(nome_usuario, email_usuario, setor_usuario, tipo_mensagem):
    
    # Renderiza o modelo HTML como uma string
    html_content = render_to_string('email_templates/email_template.html',
                                    {'nome': nome_usuario,
                                     'setor': setor_usuario,
                                     'tipo_mensagem': tipo_mensagem,
                                     })
    
    # Converte o HTML para texto sem formatação
    text_content = strip_tags(html_content)

    if tipo_mensagem == 'Aprovado':
        mensagem = 'Solicitação de Compra Aprovada | Cabana Clube'
    else:
        mensagem = 'Solicitação de Compra Reprovada | Cabana Clube'

    # Cria o e-mail
    email = EmailMultiAlternatives(
        mensagem,  # Assunto
        text_content,  # Corpo do e-mail em texto sem formatação
        settings.EMAIL_HOST_USER,  # Remetente
        [email_usuario]  # Lista de destinatários
    )
    
    # Adiciona o conteúdo HTML ao e-mail
    email.attach_alternative(html_content, "text/html")
    
    # Envia o e-mail
    email.send()