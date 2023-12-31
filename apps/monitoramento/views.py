from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from apps.monitoramento.models import Ativo
from apps.monitoramento.forms import AtivoForms
import yfinance as yf
from .tasks import checar_cotacoes
from django.contrib import messages
from django.utils.dateformat import format
import re

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
    if not request.user.is_authenticated:
        return redirect('login')
    
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
        messages.error(
            request, "Você precisa estar logado para adicionar um ativo.")
        return redirect('login')

    form = AtivoForms(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if not is_valid_ticker(form.cleaned_data['codigo']):
            messages.error(request, "Código do ticker inválido.")
            return redirect('index')

        ticker_data = yf.Ticker(form.cleaned_data['codigo'] + ".SA")

        if not ticker_data.info:
            messages.error(request, "Erro ao buscar informações do ativo.")
            return redirect('index')

        ativo = form.save(commit=False)

        # Pegando dados dos últimos 2 dias
        daily_data = ticker_data.history(period="2d")
        
        if daily_data.shape[0] == 2:  # Certificando-se de que temos dados para os dois dias
            previous_close = daily_data['Close'].iloc[0]
            current_close = daily_data['Close'].iloc[1]
            
            # Calculando a variação percentual baseado no fechamento do dia anterior e no atual
            if previous_close != 0:
                percent_variation = ((current_close - previous_close) / previous_close) * 100
                ativo.variacao_preco = percent_variation
            else:
                ativo.variacao_preco = 0
        else:
            messages.error(request, "Dados insuficientes para calcular a variação do preço.")
            return redirect('index')

        ativo.preco_atual = current_close
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
    if not request.user.is_authenticated:
        messages.error(
            request, "Você precisa estar logado para deletar um ativo.")
        return redirect('login')
    
    if request.method == "POST":
        ativo = get_object_or_404(Ativo, id=ativo_id)
        ativo_nome = ativo.nome
        ativo.delete()
        messages.success(request, f"Ativo {ativo_nome} deletado com sucesso!")
        return redirect('index')


def editar_ativo(request, ativo_id):
    if not request.user.is_authenticated:
        messages.error(
            request, "Você precisa estar logado para editar um ativo.")
        return redirect('login')
    ativo = get_object_or_404(Ativo, id=ativo_id)

    if request.method == "POST":
        form = AtivoForms(request.POST, instance=ativo)

        if form.is_valid():
            form.save()
            messages.success(
                request, f"Ativo {ativo.nome} editado com sucesso!")
            return redirect('index')
        else:
            messages.error(
                request, "Erro ao editar o ativo. Por favor, tente novamente.")


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
            'ultima_atualizacao': f"Última atualização: {formatted_date}",
            'variacao_preco': ativo.variacao_preco
        }

    return JsonResponse(data)


def is_valid_ticker(ticker):
    pattern = re.compile(r'^[A-Z]{4}.{1,}$')
    return bool(pattern.match(ticker))


def get_dates_and_prices_for_range(codigo, range):
    ticker = yf.Ticker(codigo + ".SA")
    history = ticker.history(period=range)
    dates = history.index.strftime('%Y-%m-%d').tolist()
    prices = history['Close'].tolist()
    return dates, prices


def get_data(request, codigo, range):
    # Convertir a entrada range em formato yfinance
    period_map = {
        "5d": "5d",
        "30d": "1mo",
        "6m": "6mo",
        "1y": "1y",
        "5y": "5y"
    }

    # Default para 1 ano se a entrada não for válida
    period = period_map.get(range, "1y")
    dates, prices = get_dates_and_prices_for_range(codigo, period)

    return JsonResponse({
        'dates': dates,
        'prices': prices
    })


def get_financial_indicators(request, ticker_symbol):
    ticker = yf.Ticker(ticker_symbol + ".SA")

    # Coletando informações do ticker
    info = ticker.info

    # Calculando Margem Bruta se os dados estiverem disponíveis
    gross_margin = None
    if info.get('grossProfits') and info.get('totalRevenue'):
        gross_margin = info['grossProfits'] / info['totalRevenue']

    return JsonResponse({
        # Valuation
        'marketCap': info.get('marketCap', None),
        'enterpriseValue': info.get('enterpriseValue', None),
        'trailingPE': info.get('trailingPE', None),
        'forwardPE': info.get('forwardPE', None),
        'priceToSalesTrailing12Months': info.get('priceToSalesTrailing12Months', None),
        'priceToBook': info.get('priceToBook', None),
        'dividendRate': info.get('dividendRate', None),
        'dividendYield': info.get('dividendYield', None),
        'fiveYearAvgDividendYield': info.get('fiveYearAvgDividendYield', None),
        'pegRatio': info.get('pegRatio', None),

        # Endividamento
        'totalDebt': info.get('totalDebt', None),
        'debtToEquity': info.get('debtToEquity', None),
        'totalCash': info.get('totalCash', None),
        'totalCashPerShare': info.get('totalCashPerShare', None),
        'quickRatio': info.get('quickRatio', None),
        'currentRatio': info.get('currentRatio', None),

        # Eficiência
        'grossMargin': gross_margin,
        'profitMargins': info.get('profitMargins', None),  # Margem Líquida
        'operatingMargins': info.get('operatingMargins', None),  # Margem EBIT
        'ebitdaMargins': info.get('ebitdaMargins', None),  # Margem EBITDA


        # Rentabilidade
        'returnOnAssets': info.get('returnOnAssets', None),
        'returnOnEquity': info.get('returnOnEquity', None),

        # Crescimento
        'earningsGrowth': info.get('earningsGrowth', None),
        'revenueGrowth': info.get('revenueGrowth', None),
        '52WeekChange': info.get('52WeekChange', None),
    })
