#!/usr/bin/env python3
from yahoo_finance import Share
from decimal import Decimal
import requests

stocks = {
        'AMZN': 940,
        'TSLA': 105,
#        'EPA:ODET': 900
        }

def send_mail(item, curr_value, threshold):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox3cbc324a306047c9ac421591ff64d68d.mailgun.org/messages",
        auth=("api", "key-6dd59912fd333e2fae06ce4f2f2f11cf"),
        #data={"from": "Ludovic <postmaster@sandbox3cbc324a306047c9ac421591ff64d68d.mailgun.org>",
        data={"from": "Ludovic <ludovic.aelbrecht@gmail.com>",
              "to": "Ludovic <ludovic.aelbrecht@gmail.com>, ludovic@redhat.com",
              "subject": "==> %s stocks drop: %d <= %d" % (item, curr_value, threshold),
              "text": "https://www.google.com/finance?q=%s" % (item)})
    # You can see a record of this email in your logs: https://mailgun.com/app/logs .

def near(base_number, value):
    higher_pct = base_number * 1.10
    lower_pct = base_number - (base_number * 0.10)
    if value >= lower_pct and value <= higher_pct:
        print("%d is within 10 of %d (%d<->%d)" % (value, base_number, lower_pct, higher_pct))
        return True
    else:
        print("%d is not within 10 of %d (%d<->%d)" % (value, base_number, lower_pct, higher_pct))
        return False


#disabled these -- they work, but make the output verbose:
#assert near(10, 9)
#assert near(10, 11)
#assert not near(10, 8)
#assert not near(10, 12)


def check_rate(item, curr_value, threshold):
    #if int(curr_value) <= threshold:
    if near(int(curr_value), threshold):
        print("!!!!! %s is near %d, at %f" % (item, threshold, curr_value))
        send_mail(item, curr_value, threshold)
    else:
        print("%s is at %f, far from %d" % (item, curr_value, threshold))


# special case for BTC value lookup:
url = 'http://api.coindesk.com/v1/bpi/currentprice.json'
r = requests.get(url, headers={'Accept': 'application/json'})
btc_eur = Decimal(r.json()['bpi']['EUR']['rate_float'])
check_rate("BTC", curr_value=btc_eur, threshold=1650)

for ticker, threshold in stocks.items():
    print("ticker %s, threshold %d" % (ticker, threshold))
    try:
        price = Decimal(Share(ticker).get_days_low())
    except:
        price = Decimal(Share(ticker).get_days_low())
    check_rate(ticker, curr_value=price, threshold=threshold)

