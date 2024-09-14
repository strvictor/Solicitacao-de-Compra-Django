from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Dados
import datetime

def mostra_form(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        setor = request.POST.get('setor')
        prioridade = request.POST.get('prioridade')
        data_limite = request.POST.get('data_limite')
        descricao = request.POST.get('descricao')
        arquivo = request.FILES.get('arquivo')
        data_e_hora_atual = datetime.datetime.now()
        
        dados = Dados(nome=nome, email=email, telefone=telefone, setor=setor, prioridade=prioridade, data_limite=data_limite, descricao=descricao, arquivo=arquivo, data_pedido=data_e_hora_atual)
        dados.save()

        # Adiciona a mensagem de sucesso
        messages.success(request, 'Seu pedido foi enviado com sucesso!')
        
        return redirect('/')
    
    return render(request, 'index.html')
