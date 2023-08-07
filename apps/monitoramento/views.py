from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from apps.monitoramento.models import Ativo
from apps.monitoramento.forms import AtivoForms
import yfinance as yf
from .tasks import checar_cotacoes

MAPEAMENTO_SETORES = {
    "Consumer Cyclical": "CONSUMER_CYCLICAL",
    "Consumer Defensive": "CONSUMER_DEFENSIVE",
    "Utilities": "UTILITIES",
    "Industrials": "INDUSTRIALS",
    "Basic Materials": "BASIC_MATERIALS",
    "Financial Services": "FINANCIAL_SERVICES",
    "Technology": "TECHNOLOGY",
    "Healthcare": "HEALTHCARE",
    "Energy": "ENERGY",
    "Communication Services": "COMMUNICATION_SERVICES",
    
}

def index(request):
    if request.user.is_authenticated:
        # Se o usuário estiver logado, obtenha seus ativos
        ativos = Ativo.objects.filter(usuario=request.user).order_by('-id')
    else:
        # Se o usuário não estiver logado, não mostre nenhum ativo
        ativos = []

    form = AtivoForms()

    return render(request, 'index.html', {'cards': ativos, 'form': form})


def detalhes_ativo(request, ativo_id):
    ativo = get_object_or_404(Ativo, pk=ativo_id)
    return render(request, 'detalhes_ativo.html', {'ativo': ativo})

def novo_ativo(request):
    if not request.user.is_authenticated:
        return redirect('login')  # ou alguma outra resposta caso o usuário não esteja logado

    form = AtivoForms(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ticker_data = yf.Ticker(form.cleaned_data['codigo'] + ".SA")
        
        ativo = form.save(commit=False)
        ativo.preco_atual = ticker_data.history(period="1d")['Close'].iloc[0]
        ativo.nome = ticker_data.info.get('longName', None)
        ativo.setor = MAPEAMENTO_SETORES.get(ticker_data.info.get('sector'), None)
        ativo.descricao = ticker_data.info.get('longBusinessSummary', None)

        # Vincula o usuário logado ao ativo
        ativo.usuario = request.user
        
        ativo.save()
        return redirect('index')

def deletar_ativo(request, ativo_id):
    if request.method == "POST":
        ativo = get_object_or_404(Ativo, id=ativo_id)
        ativo.delete()
        return redirect('index')

def editar_ativo(request, ativo_id):
    # Busca o ativo pelo ID ou lança uma exceção 404 se não for encontrado
    ativo = get_object_or_404(Ativo, id=ativo_id)
    
    # Se a requisição for POST, tentamos atualizar o ativo
    if request.method == "POST":
        form = AtivoForms(request.POST, instance=ativo)  # passamos a instância do ativo para atualizar o objeto existente
        
        if form.is_valid():
            form.save()
            return redirect('index')
        
def get_ativo_info(request, ativo_id):
    ativo = get_object_or_404(Ativo, id=ativo_id)
    data = {
        "codigo": ativo.codigo,
        "limite_inferior": str(ativo.limite_inferior),
        "limite_superior": str(ativo.limite_superior),
        "periodicidade_checagem": str(ativo.periodicidade_checagem),
    }
    return JsonResponse(data)

def test(request):
    checar_cotacoes.delay()
    return HttpResponse("Done")