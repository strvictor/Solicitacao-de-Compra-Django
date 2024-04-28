from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def autenticacao(request):
    if request.method == "GET":
        return render(request, 'login.html')
        # return HttpResponse('GET EM AUTENTICACAO')
    
    elif request.method == "POST":
        return HttpResponse('POST EM AUTENTICACAO')