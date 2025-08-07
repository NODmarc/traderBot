def generate_signals(df):
    last = df.iloc[-1]
    rsi = last["RSI"]
    ema20 = last["EMA20"]
    ema50 = last["EMA50"]
    close = last["close"]
    adx = last["ADX"]
    plus_di = last["+DI"]
    minus_di = last["-DI"]
    macd = last["MACD"]
    signal = last["MACD_signal"]

    # --- Проверка наличия тренда (ADX) ---
    if adx < 20:
        return "NO_TREND"

    # --- RSI фильтры ---
    if rsi > 70:
        return "RSI - AVOID_BUY"
    elif rsi < 30:
        return "RSI - AVOID_SELL"

    # --- MACD сигналы ---
    macd_signal = None
    if signal > 0 and 0 < macd < signal:
        macd_signal = "MACD - STRONG_BUY"
    elif signal < 0 and 0 > macd > signal:
        macd_signal = "MACD - STRONG_SELL"
    elif 0 < signal < macd and macd > 0:
        macd_signal = "MACD - BUY"
    elif 0 > signal > macd and macd < 0:
        macd_signal = "MACD - SELL"
    elif (signal > 0 > macd and signal > macd) or (signal < 0 < macd and signal < macd):
        macd_signal = "MACD - NEUTRAL"

    # --- Комбинирование MACD с EMA и RSI ---
    if macd_signal == "STRONG_BUY" and close > ema20 > ema50 and rsi > 50 and plus_di > minus_di:
        return "MACD с EMA и RSI  - STRONG_BUY"
    elif macd_signal == "STRONG_SELL" and close < ema20 < ema50 and rsi < 50 and minus_di > plus_di:
        return "MACD с EMA и RSI  - STRONG_SELL"
    elif macd_signal == "BUY" and close > ema20 and rsi > 50:
        return "MACD с EMA и RSI - BUY"
    elif macd_signal == "SELL" and close < ema20 and rsi < 50:
        return "MACD с EMA и RSI - SELL"
    elif macd_signal == "NEUTRAL":
        return "MACD с EMA и RSI - HOLD"

    return "HOLD"
