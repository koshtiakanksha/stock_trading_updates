import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = "Yours"
news_api_key = "Yours"

account_sid = "Yours"
auth_token = "Yours"
phone_number = "Yours"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(day_before_yesterday_closing_price) - float(yesterday_closing_price))

diff_percentage = (difference / float(yesterday_closing_price)) * 100

if diff_percentage > 5:
    news_params = {
        "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_article = [f"Headline: {article['title']}. \nBrief: {article['description']}"
                         for article in three_articles]
    client = Client(account_sid, auth_token)

    for i in range(3):
        message = client.messages.create(
            body=formatted_article[i],
            from_=phone_number,
            to='receiver number'
        )
        print(message.status)
