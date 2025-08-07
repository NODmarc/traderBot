import numpy as np
import pandas as pd

def add_indicators(df):
# EMA, RSI, MACD
    # Экспоненциальная скользящая средняя
    df["EMA20"] = df["close"].ewm(span=20).mean()
    df["EMA50"] = df["close"].ewm(span=50).mean()
    df["EMA120"] = df["close"].ewm(span=120).mean()
    df["EMA200"] = df["close"].ewm(span=200).mean()

    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    exp1 = df["close"].ewm(span=12).mean()
    exp2 = df["close"].ewm(span=26).mean()
    df["MACD"] = exp1 - exp2
    df["MACD_signal"] = df["MACD"].ewm(span=9).mean()

    # ADX (+DI и -DI)
    # Индекс среднего направления (силы тренда)
    high = df["high"]
    low = df["low"]
    close = df["close"]

    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm = plus_dm.where(plus_dm > 0, 0)
    minus_dm = minus_dm.where(minus_dm < 0, 0)

    tr = pd.concat([
        high - low,
        abs(high - close.shift()),
        abs(low - close.shift())
    ], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()

    plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
    minus_di = 100 * (abs(minus_dm.rolling(14).mean()) / atr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    df["ADX"] = dx.rolling(14).mean()
    df["+DI"] = plus_di
    df["-DI"] = minus_di

    # Профиль объема
    bin_size = (df["high"].max() - df["low"].min()) / 25
    bins = np.arange(df["low"].min(), df["high"].max(), bin_size)
    df["price_bin"] = pd.cut(df["close"], bins)
    volume_profile = df.groupby("price_bin", observed=False)["volume"].sum()
    poc_bin = volume_profile.idxmax()
    poc_price = poc_bin.mid

    # Метки по сессиям
    df["weekday"] = df.index.weekday
    df["hour"] = df.index.hour
    df["is_weekend"] = df["weekday"].isin([5, 6])
    df["is_us_session"] = df["hour"].between(15, 21)

    # Расчет вероятностей
    last = df.iloc[-1]
    conditions = [
        last["close"] > last["EMA20"],
        last["EMA20"] > last["EMA50"],
        last["MACD"] > last["MACD_signal"],
        last["RSI"] > 50,
        last["ADX"] > 25,
        last["close"] > poc_price,
        last["is_us_session"] and not last["is_weekend"],
        not (last["RSI"] > 70 or last["RSI"] < 30)  # не входить против тренда
    ]
    prob_up = round(np.mean(conditions), 2)
    prob_down = round(1 - prob_up, 2)
    df.loc[df.index[-1], "prob_up"] = prob_up
    df.loc[df.index[-1], "prob_down"] = prob_down
    return df