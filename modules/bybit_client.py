import requests
import pandas as pd
from datetime import datetime, timezone

# Получить текущее UTC-время
now = datetime.now(timezone.utc)

# Получить Unix-время в миллисекундах
current_date_epoch_s = int(now.timestamp())

print("Now:", now)
print("Current date - Epoch time (ms):", current_date_epoch_s)

def get_kline(symbol, interval, limit):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()["result"]["list"]
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "turnover"
    ])
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    df["timestamp"] = pd.to_datetime(pd.to_numeric(df["timestamp"]), unit='ms')
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    # print(df)
    return df

# result = get_kline("BTCUSDT", 60, 300)
# print(result)

