import sys
import urllib2
import pprint
import ujson
import time
import traceback
import subprocess

def sendData(timestamp, name, value):
    cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local." + name, value, timestamp)
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]

while True:
    try:
        start = time.time()

        base_url = "https://www.bitstamp.net/api/v2/order_book/btcusd/"
        bitstamp_btcusd = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        bitstamp_btcusd_asks = [float(x[0]) for x in bitstamp_btcusd['asks']]
        bitstamp_btcusd_bids = [float(x[0]) for x in bitstamp_btcusd['bids']]
        
        # base_url = "https://api.kraken.com/0/public/Depth?pair=xbtusd&count=5"
        # kraken_btcusd = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())['result']['XXBTZUSD']
        # kraken_btcusd_asks = [float(x[0]) for x in kraken_btcusd['asks']]
        # kraken_btcusd_bids = [float(x[0]) for x in kraken_btcusd['bids']]
        kraken_btcusd_asks = [0]
        kraken_btcusd_bids = [0]
        
        base_url = "https://api.gdax.com/products/BTC-USD/book"
        gdax_btcusd = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        gdax_btcusd_asks = [float(x[0]) for x in gdax_btcusd['asks']]
        gdax_btcusd_bids = [float(x[0]) for x in gdax_btcusd['bids']]

        base_url = "https://api.bitfinex.com/v1/book/btcusd"
        bitfinex_btcusd = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        bitfinex_btcusd_asks = [float(x['price']) for x in bitfinex_btcusd['asks']]
        bitfinex_btcusd_bids = [float(x['price']) for x in bitfinex_btcusd['bids']]

        base_url = "https://api.gemini.com/v1/book/btcusd"
        gemini_btcusd = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        gemini_btcusd_asks = [float(x['price']) for x in gemini_btcusd['asks']]
        gemini_btcusd_bids = [float(x['price']) for x in gemini_btcusd['bids']]

        base_url = "https://api.bitfinex.com/v1/book/ethbtc"
        bitfinex_ethbtc = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        bitfinex_eth_asks = [float(x['price']) for x in bitfinex_ethbtc['asks']]
        bitfinex_eth_bids = [float(x['price']) for x in bitfinex_ethbtc['bids']]

        base_url = "https://api.gemini.com/v1/book/ethbtc"
        gemini_ethbtc = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        gemini_eth_asks = [float(x['price']) for x in gemini_ethbtc['asks']]
        gemini_eth_bids = [float(x['price']) for x in gemini_ethbtc['bids']]

        base_url = "https://api.bithumb.com/public/orderbook/ETH"
        korea_eth = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        korea_eth_asks = [int(x['price']) for x in korea_eth['data']['asks']]
        korea_eth_bids = [int(x['price']) for x in korea_eth['data']['bids']]

        base_url = "https://api.bithumb.com/public/orderbook/BTC"
        korea_btc = ujson.loads(urllib2.urlopen(base_url, timeout=10).read())
        korea_btc_asks = [int(x['price']) for x in korea_btc['data']['asks']]
        korea_btc_bids = [int(x['price']) for x in korea_btc['data']['bids']]

        most_recent_korea_eth_ask = korea_eth_asks[0]
        most_recent_korea_eth_bid = korea_eth_bids[0]
        most_recent_korea_btc_ask = korea_btc_asks[0]
        most_recent_korea_btc_bid = korea_btc_bids[0]
        most_recent_gemini_eth_ask = gemini_eth_asks[0]
        most_recent_gemini_eth_bid = gemini_eth_bids[0]
        most_recent_bitfinex_eth_bid = bitfinex_eth_bids[0]
        most_recent_bitfinex_eth_ask = bitfinex_eth_asks[0]
        most_recent_bitfinex_bitcusd_ask = bitfinex_btcusd_asks[0]
        most_recent_bitfinex_bitcusd_bid = bitfinex_btcusd_bids[0]
        most_recent_gemini_bitcusd_ask = gemini_btcusd_asks[0]
        most_recent_gemini_bitcusd_bid = gemini_btcusd_bids[0]
        most_recent_gdax_btcusd_ask = gdax_btcusd_asks[0]
        most_recent_gdax_btcusd_bid = gdax_btcusd_bids[0]
        most_recent_bitstamp_bitcusd_ask = bitstamp_btcusd_asks[0]
        most_recent_bitstamp_bitcusd_bid = bitstamp_btcusd_bids[0]
        most_recent_kraken_btcusd_ask = kraken_btcusd_asks[0]
        most_recent_kraken_btcusd_bid = kraken_btcusd_bids[0]
        
        timestamp = time.time()
        
        with open("raw.csv", "a") as f:
            f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (timestamp, 
                                                                            most_recent_korea_eth_ask,
                                                                            most_recent_korea_eth_bid,
                                                                            most_recent_korea_btc_ask,
                                                                            most_recent_korea_btc_bid,
                                                                            most_recent_gemini_eth_ask,
                                                                            most_recent_gemini_eth_bid,
                                                                            most_recent_bitfinex_eth_ask,
                                                                            most_recent_bitfinex_eth_bid,
                                                                            most_recent_bitfinex_bitcusd_ask,
                                                                            most_recent_bitfinex_bitcusd_bid,
                                                                            most_recent_gemini_bitcusd_ask,
                                                                            most_recent_gemini_bitcusd_bid,
                                                                            most_recent_gdax_btcusd_ask,
                                                                            most_recent_gdax_btcusd_bid,
                                                                            most_recent_bitstamp_bitcusd_ask,
                                                                            most_recent_bitstamp_bitcusd_bid,
                                                                            most_recent_kraken_btcusd_ask,
                                                                            most_recent_kraken_btcusd_bid
                                                                            ))
                                                                            
            f.write('\n')

        sendData(timestamp, 'most_recent_korea_eth_ask', most_recent_korea_eth_ask)
        sendData(timestamp, 'most_recent_korea_eth_bid', most_recent_korea_eth_bid)
        sendData(timestamp, 'most_recent_korea_btc_ask', most_recent_korea_btc_ask)
        sendData(timestamp, 'most_recent_korea_btc_bid', most_recent_korea_btc_bid)
        sendData(timestamp, 'most_recent_gemini_eth_ask', most_recent_gemini_eth_ask)
        sendData(timestamp, 'most_recent_gemini_eth_bid', most_recent_gemini_eth_bid)
        sendData(timestamp, 'most_recent_bitfinex_eth_ask', most_recent_bitfinex_eth_ask)
        sendData(timestamp, 'most_recent_bitfinex_eth_bid', most_recent_bitfinex_eth_bid)
        sendData(timestamp, 'most_recent_bitfinex_bitcusd_ask', most_recent_bitfinex_bitcusd_ask)
        sendData(timestamp, 'most_recent_bitfinex_bitcusd_bid', most_recent_bitfinex_bitcusd_bid)
        sendData(timestamp, 'most_recent_gemini_bitcusd_ask', most_recent_gemini_bitcusd_ask)
        sendData(timestamp, 'most_recent_gemini_bitcusd_bid', most_recent_gemini_bitcusd_bid)
        sendData(timestamp, 'most_recent_gdax_btcusd_ask', most_recent_gdax_btcusd_ask)
        sendData(timestamp, 'most_recent_gdax_btcusd_bid', most_recent_gdax_btcusd_bid)
        sendData(timestamp, 'most_recent_bitstamp_bitcusd_ask', most_recent_bitstamp_bitcusd_ask)
        sendData(timestamp, 'most_recent_bitstamp_bitcusd_bid', most_recent_bitstamp_bitcusd_bid)
        sendData(timestamp, 'most_recent_kraken_btcusd_ask', most_recent_kraken_btcusd_ask)
        sendData(timestamp, 'most_recent_kraken_btcusd_bid', most_recent_kraken_btcusd_bid)

        end = time.time() - start
        sendData(timestamp, 'runtime', end)
        
        # BLUE: Sell BTC for KRW in Korea, buy ETH with KRA in Korea, transfer ETH to US, sell ETH in US for BTC
        # krw = btcAmt * most_recent_korea_btc_bid * (1 - .000025)  # With coupons
        # eth = krw / most_recent_korea_eth_ask * (1 - .000025)  # With coupons
        # eth = eth - .01
        # btc = most_recent_gemini_eth_bid * eth * (1 - .0015) # As a maker
        # gain = btc - btcAmt
        # gain = gain * btcPrice

        # alias(
        #     offset(
        #         scale(
        #             multiplySeries(*.most_recent_gemini_eth_bid,
        #                 offset(
        #                     divideSeries(
        #                         scale(
        #                             scale(
        #                                 timeShift(*.most_recent_korea_btc_bid, "-20min"), 0.5)
        #                         , 0.9985),
        #                         scale(timeShift(*.most_recent_korea_eth_ask, "-20min"), 0.9985)
        #                 ), -0.01)
        #             ),
        #         0.9975),
        #      -0.5),
        #     "Buy Korea, sell US"
        # )

        # RED: Buy ETH in US, sell ETH for KRW in Korea, buy BTC for KRW in Korea, transfer BTC to US, sell BTC in US for ETH
        # eth = btcAmt / most_recent_gemini_eth_ask * (1 - .0025) # As a maker
        # krw = eth * most_recent_korea_eth_bid  * (1 - .0015) # With coupons
        # btc = krw / most_recent_korea_btc_ask * (1 - .0015) # With coupons
        # btc = btc - .0005
        # gain = btc - btcAmt
        # gain = gain * btcPrice
            
        # alias(
        #    offset(
        #        offset(
        #            divideSeries(
        #                    multiplySeries(
        #                            scale(scale(invert(timeShift(*.most_recent_gemini_eth_ask, "-10min")), 0.5), 0.9975),
        #                            scale(*.most_recent_korea_eth_bid, 0.9985)
        #                    ),
        #             scale(*.most_recent_korea_btc_ask, 0.9985))
        #         , -0.0005)
        #     , -0.5)
        # ,"Buy US, Sell Korea")

    except Exception as e:
        traceback.print_exc()
        time.sleep(20)
        print e

# # For Gemini making -> Bitthumb
# #total = 1 - (buyPrice + buyPrice * .002) / (sellPrice + sellPrice * .0015) - .0005
# #print total
#
# # For Gemini market making
# #print 1 - (buyPrice + buyPrice * .001) / (sellPrice + sellPrice * .001)
"""
- When regular people buy and sell, they'll probably do that in round numbers.
- Monitor all exchanges for movements. When the biggest exchanges move, the smaller ones should follow suit. Informed!
- Buy BTC/ETH on margin in korea, simultaneously sell BTC/ETH on margin in US. Transfer margin to Korea and pocket the difference. No risk!
    KOREA LOW, USA HIGH
    15:1        5:1

    1. Korea loans me 1 BTC. I buy ETH with the BTC. I get 15 ETH.
    2. USA loans me 5 ETH. I buy BTC for ETH. I get 1 BTC.
    3. I transfer 1 BTC to Korea to pay off loan
    4. I transfer 15 ETH to USA and pay off 5 ETH loan
    5. Net: 10 ETH
    ZERO market risk. No prediction needed.
"""
