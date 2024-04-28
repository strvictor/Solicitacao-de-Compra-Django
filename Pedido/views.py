from django.shortcuts import render
from django.http import HttpResponse
from .models import Dados
import datetime

# Create your views here.
def mostra_form(request):
    if request.method == "GET":
        return render(request, 'index.html')
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        setor = request.POST.get('setor')
        prioridade = request.POST.get('prioridade')
        data_limite = request.POST.get('data_limite')
        descricao = request.POST.get('descricao')
        arquivo = request.FILES['arquivo']
        data_e_hora_atual = datetime.datetime.now()
            
        # chama a classe do banco de dados
        dados = Dados(nome=nome, email=email, telefone=telefone, setor=setor, prioridade=prioridade, data_limite=data_limite, descricao=descricao, arquivo=arquivo, data_pedido=data_e_hora_atual)

        # envia os dados do formulario (nesse momento não estou tratando os dados!)
        dados.save()

        # # Faça o que desejar com o arquivo, por exemplo, salve-o no disco
        # path_destino = 'C:\\Users\\P. Victor - TI\\Desktop\\' + arquivo.name
        # print(path_destino)
        # with open(path_destino, 'wb') as destino:
        #     for parte in arquivo.chunks():
        #         destino.write(parte)

        return HttpResponse('Dados salvos no banco de dados')