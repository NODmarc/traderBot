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
    1. Determine whether the market is trending or ranging using ADX. (ADX > 25 = trend, ADX > 50 = strong trend)
    2. Identify trend direction using +DI and -DI, and EMA alignment (EMA20 vs EMA50 and EMA50 vs EMA200).
    3. Interpret RSI: overbought (RSI > 70), oversold (RSI < 30), buy signal (RSI > 50), sell signal (RSI < 50).
    4. Evaluate MACD vs MACD Signal for momentum confirmation.
    5. Consider the provided probabilities (if available) for final bias.
    6. Provide a concise summary of the market condition.
    7. Give a clear trading suggestion (Buy, Sell, Hold, Avoid) with brief justification.
    8. Specify the entry point (buy or sell) for the most probable scenario.
    9. Define stop-loss and take-profit levels:
    - Use nearby support and resistance zones.
    - Apply Fibonacci tools: retracement, projection, or correction.
    - Place stop-loss beyond the nearest low or high.
    - Set take-profit at the next target level based on trend or Fibonacci.

    Additional formatting rules:
    - Do not use Markdown formatting.
    - Use emojis to enhance clarity and engagement.
    - At the end of your response, include three relevant hashtags.

    Your response should be practical and focused on short-term trading.
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





