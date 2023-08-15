import yfinance as yf

def fetch_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    return info

if __name__ == "__main__":
    symbol = "WEGE3.SA"
    data = fetch_data(symbol)

    # Imprime os dados em um formato legível
    for key, value in data.items():
        print(f"{key}: {value}")

    # Você pode também exportar os dados para um arquivo JSON, se preferir:
    # import json
    # with open('PETR4_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
