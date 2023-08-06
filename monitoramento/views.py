from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def detalhes_ativo(request):
    return render(request, 'detalhes_ativo.html')
