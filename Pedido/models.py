from django.db import models

# Create your models here.
class Dados(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    prioridade = models.CharField(max_length=100)
    data_limite = models.DateField(max_length=50)
    descricao = models.CharField(max_length=1000)
    arquivo = models.FileField(null=True, upload_to='uploads/')
    data_pedido = models.DateTimeField()
    status = models.CharField(max_length=50, default='Pendente')
    estagio = models.CharField(max_length=50, default='1/5')
    ultima_atualizacao = models.CharField(max_length=50, default='-')
    acao = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return self.nome
    
class UsuariosBD(models.Model):
    setor = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self) -> str:
        return self.nome