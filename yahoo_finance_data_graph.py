import requests
import pandas as pd

def get_historical_data(symbol, start_date, end_date):
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(url)
        return data
    else:
        print("Failed to retrieve data")
        return None

def get_current_price(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        start_index = response.text.find('"regularMarketPrice":{"raw":') + len('"regularMarketPrice":{"raw":')
        end_index = response.text.find(',', start_index)
        price = response.text[start_index:end_index]
        return float(price)
    else:
        print("Failed to retrieve data")
        return None


def get_dividend_yield(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        start_index = response.text.find('"trailingAnnualDividendYield":{"raw":') + len('"trailingAnnualDividendYield":{"raw":')
        end_index = response.text.find(',', start_index)
        yield_value = response.text[start_index:end_index]
        return float(yield_value)
    else:
        print("Failed to retrieve data")
        return None

symbol = "AAPL"
start_date = "946684800" # January 1, 2000
end_date = "1654060800" # February 1, 2022

historical_data = get_historical_data(symbol, start_date, end_date)
current_price = get_current_price(symbol)
dividend_yield = get_dividend_yield(symbol)


# run
print(f"Stock: {symbol}")
print(f"Current price: {current_price:.2f}")
print(f"annual dividend yield: {dividend_yield:.2f}%")

if historical_data is not None:
    print("Historical data:")
    print(historical_data.head())
else:
    print("Failed to retrieve historical data")