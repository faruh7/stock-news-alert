import requests
import smtplib
MY_EMAIL = "BLAH.BLAH@gmail.com"
MY_PASSWORD = "PASSWORD"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "58558855855858855585"
ALPHA_API = "GJHGJGHJHGJH"
parameter_news = {
    "q": "tesla",
    "from": "2022-01-01",
    "sortBy": "publishedAt",
    "apiKey": NEWS_API,
    "language": "en",
    "qInTitle": COMPANY_NAME,
}
parameter_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API,
}
r = requests.get(url=STOCK_ENDPOINT, params=parameter_price)
data = r.json()["Time Series (Daily)"]
new_list = list(data.items())
yesterday = float(new_list[0][1]['4. close'])
before_yesterday = float(new_list[1][1]['4. close'])
inc_or_decr = 1 - (yesterday/before_yesterday)

if inc_or_decr > 0.04 or inc_or_decr < -0.04:
    r2 = requests.get(url=NEWS_ENDPOINT, params=parameter_news)
    data2 = r2.json()['articles'][:3]
    headlines = []
    content = []
    for i in data2:
        headlines.append(i["title"])
        content.append(i["content"][:126])

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        for k in range(0, 3):
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="SOME_EMAIL@inbox.ru",
                msg=f"Subject:Tesla news\n\nHeadline: {headlines[k]}\nContent: {content[k]}"
            )
