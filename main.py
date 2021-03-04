import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_URL = "https://www.alphavantage.co/query"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": "demo",
}

NEWS_APIKEY = "5a6d17cad5364b94a9b9539d1ffb8482"
NEWS_URL = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_APIKEY,
    "pageSize": 3,
}

ACCOUNT_SID = 0
AUTH_TOKENT = 0

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def stock():
    response = requests.get(STOCK_URL, params=STOCK_PARAMS)
    response.raise_for_status()
    data = response.json()['Time Series (Daily)']

    # for i in data:
    #     print(i['1. open']) #이건 왜 안되는 걸까?

    stock_price = 0
    stock_list = []
    for i in data:
        current_price = float(data[i]['1. open']) #이상하긴 한데 됬다.
        stock_list.append(current_price)

    for i in range(len(stock_list)):
        if stock_list[i] > stock_list[i-1]*(1.05) or stock_list[i] < stock_list[i-1]*(0.95):
            print("Get News")


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def get_news():
    news_response = requests.get(NEWS_URL, params=NEWS_PARAMS)
    news_response.raise_for_status()
    news_data = news_response.json()
    for i in news_data['articles']:
        send_msg(f"Headline: {i['title']}\nBrief: {i['description']}\n")

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_msg(msg):
    client = Client(ACCOUNT_SID, AUTH_TOKENT)
    message = client.messages \
        .create(
        body=msg,
        from_='+15103302089',
        to='+'
    )
    print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

