import sys
import urllib2
import pprint
import ujson
import time

btcPrice = 4050
btcAmt = float(sys.argv[1])

base_url = "https://api.gemini.com/v1/book/ethbtc"
us_ethbtc = ujson.loads(urllib2.urlopen(base_url).read())
us_eth_asks = [float(x['price']) for x in us_ethbtc['asks']]
us_eth_bids = [float(x['price']) for x in us_ethbtc['bids']]

base_url = "https://api.bithumb.com/public/orderbook/ETH"
korea_eth = ujson.loads(urllib2.urlopen(base_url).read())
korea_eth_asks = [int(x['price']) for x in korea_eth['data']['asks']]
korea_eth_bids = [int(x['price']) for x in korea_eth['data']['bids']]

base_url = "https://api.bithumb.com/public/orderbook/BTC"
korea_btc = ujson.loads(urllib2.urlopen(base_url).read())
korea_btc_asks = [int(x['price']) for x in korea_btc['data']['asks']]
korea_btc_bids = [int(x['price']) for x in korea_btc['data']['bids']]

most_recent_korea_eth_ask = korea_eth_asks[0]
most_recent_korea_eth_bid = korea_eth_bids[0]
most_recent_korea_btc_ask = korea_btc_asks[0]
most_recent_korea_btc_bid = korea_btc_bids[0]
most_recent_us_eth_ask = us_eth_asks[0]
most_recent_us_eth_bid = us_eth_bids[0]

# BLUE: Buy ETH in Korea, sell ETH in US
krw = most_recent_korea_btc_bid * btcAmt * (1 - .0015)
eth = krw / most_recent_korea_eth_ask * (1 - .0015)
eth = eth - .01
btc = ((eth * (1 - .0025)) * most_recent_us_eth_bid)
gain = btc - btcAmt

with open("ticker.csv", "a") as f:
    f.write("BLUES, %s, %s") % time.time(), gain * btcPrice
print time.time(), "BLUES (Korea -> US): $" + str(gain * btcPrice)

# RED: Buy ETH in US, sell ETH in Korea, transfer BTC to US
eth = (btcAmt * (1 - .0025)) / most_recent_us_eth_ask
krw = (eth * (1 - .0015)) * most_recent_korea_eth_ask
btc = krw * (1 - .0015) / most_recent_korea_btc_bid
btc = btc - .0005
gain = btc - btcAmt
with open("ticker.csv", "a") as f:
    f.write("REDS, %s, %s") % time.time(), gain * btcPrice
print time.time(), "REDS (US -> Korea -> US): $" + str(gain * btcPrice)

# # For Gemini making -> Bitthumb
# #total = 1 - (buyPrice + buyPrice * .002) / (sellPrice + sellPrice * .0015) - .0005
# #print total
#
# # For Gemini market making
# #print 1 - (buyPrice + buyPrice * .001) / (sellPrice + sellPrice * .001)
