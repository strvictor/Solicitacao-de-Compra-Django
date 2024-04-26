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
    arquivo = models.FileField()

    def __str__(self) -> str:
        return self.nome
    
class Coodernadores(models.Model):
    setor = models.CharField(max_length=100)
    nome_coodernador = models.CharField(max_length=100)
    email_coodernador = models.EmailField(max_length=100)

    def __str__(self) -> str:
        return self.nome_coodernador