import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "FP4SMHAQ5SYPXE9U"
NEWS_API_KEY = "5a6d17cad5364b94a9b9539d1ffb8482"

TWILIO_SID = "AC5fb6a8d0670c958f4c6d3e9f200998e0"
TWILIO_AUTH_TOKEN = "233a08259393933c5a64f30f20d02874"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey":STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data['4. close'])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

difference = yesterday_closing_price - day_before_yesterday_closing_price

diff_percent = round(difference / yesterday_closing_price) * 100
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+15103302089",
            to="+821055447365",
        )
