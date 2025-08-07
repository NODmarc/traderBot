from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionDeveloperMessageParam

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt_about_market(df):
    last_row = df.iloc[-1] # последняя свеча
    prompt = f"""
    You are a professional trading assistant.
    
    Analyze the current market condition using the following technical indicators:
    
    - RSI (Relative Strength Index): {last_row['RSI']:.2f}
    - EMA20: {last_row['EMA20']:.2f}
    - EMA50: {last_row['EMA50']:.2f}
    - EMA200: {last_row['EMA200']:.2f}
    - Open Price: {last_row['open']:.2f}
    - Close Price: {last_row['close']:.2f}
    - High Price: {last_row['high']:.2f}
    - Low Price: {last_row['low']:.2f}
    - ADX (Average Directional Index): {last_row['ADX']:.2f}
    - +DI: {last_row['+DI']:.2f}
    - -DI: {last_row['-DI']:.2f}
    - MACD: {last_row['MACD']:.2f}
    - MACD Signal: {last_row['MACD_signal']:.2f}
    - Prob. Up: {last_row.get('prob_up', 'N/A')}
    - Prob. Down: {last_row.get('prob_down', 'N/A')}
    
    Instructions:
    1. Is the market trending or ranging? Use ADX for this. (ADX > 25 тренд, ADX > 50 сильный тренд)
    2. Determine trend direction using +DI and -DI, and EMA alignment (EMA20 vs EMA50 and EMA50 vs EMA200) .
    3. Interpret RSI for overbought (RSI > 70), oversold (RSI < 30), buy (RSI > 50), sell (RSI < 50). 
    4. Evaluate MACD vs MACD Signal for momentum confirmation.
    5. Consider the provided probabilities (if available) for final bias.
    6. Provide a concise summary of market condition.
    7. Give a clear trading suggestion (Buy, Sell, Hold, Avoid) with brief justification.
    
    Your response should be practical and relevant to short-term trading.
    """
    messages = [
        ChatCompletionDeveloperMessageParam(role="developer", content="Отчет создать на русском языке."),
        ChatCompletionUserMessageParam(role="user", content=prompt)
    ]


    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )
    return response.choices[0].message.content





