from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from apps.monitoramento.models import Ativo
from apps.monitoramento.forms import AtivoForms
import yfinance as yf
from .tasks import checar_cotacoes
from django.contrib import messages
from django.utils.dateformat import format

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
    
    # Fetch data using yfinance
    ticker = yf.Ticker(ativo.codigo + ".SA")
    history = ticker.history(period="1y")  # Get data for 1 year, for instance.

    dates = history.index.strftime('%Y-%m-%d').tolist()
    prices = history['Close'].tolist()

    # Prepare context data
    context = {
        'ativo': ativo,
        'dates': dates,
        'prices': prices
    }

    return render(request, 'detalhes_ativo.html', context)

def novo_ativo(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para adicionar um ativo.")
        return redirect('login')

    form = AtivoForms(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ticker_data = yf.Ticker(form.cleaned_data['codigo'] + ".SA")

        if not ticker_data.info:
            messages.error(request, "Erro ao buscar informações do ativo.")
            return redirect('index')
        
        ativo = form.save(commit=False)
        ativo.preco_atual = ticker_data.history(period="1d")['Close'].iloc[0]
        ativo.nome = ticker_data.info.get('longName', None)
        ativo.setor = MAPEAMENTO_SETORES.get(ticker_data.info.get('sector'), None)
        ativo.descricao = ticker_data.info.get('longBusinessSummary', None)
        ativo.usuario = request.user
        ativo.save()
        messages.success(request, f"O Ativo {ativo.codigo} foi adicionado com sucesso!")
    else:
        messages.error(request, "Erro ao adicionar o ativo. Por favor, tente novamente.")

    return redirect('index')

def deletar_ativo(request, ativo_id):
    if request.method == "POST":
        ativo = get_object_or_404(Ativo, id=ativo_id)
        ativo_nome = ativo.nome
        ativo.delete()
        messages.success(request, f"Ativo {ativo_nome} deletado com sucesso!")
        return redirect('index')

def editar_ativo(request, ativo_id):
    ativo = get_object_or_404(Ativo, id=ativo_id)
    
    if request.method == "POST":
        form = AtivoForms(request.POST, instance=ativo)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"Ativo {ativo.nome} editado com sucesso!")
            return redirect('index')
        else:
            messages.error(request, "Erro ao editar o ativo. Por favor, tente novamente.")
        
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
    messages.info(request, "A tarefa de checar cotações foi iniciada.")
    return HttpResponse("Done")

def get_updated_ativos(request):
    ativos = Ativo.objects.all()
    data = {}
    
    for ativo in ativos:
        formatted_date = format(ativo.ultima_atualizacao, "d/m/Y H:i")
        data[ativo.id] = {
            'preco_atual': ativo.preco_atual,
            'ultima_atualizacao': f"Última atualização: {formatted_date}"
        }

    return JsonResponse(data)
