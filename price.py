import sys
import urllib2
import pprint
import ujson
import time
import subprocess

btcPrice = 4050
btcAmt = float(sys.argv[1])

while True:
    try:
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
        
        timestamp = time.time()
        
        with open("raw.csv", "a") as f:
            f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s" % (timestamp, most_recent_korea_eth_ask, most_recent_korea_eth_bid, most_recent_korea_btc_ask, most_recent_korea_btc_bid, most_recent_gemini_eth_ask, most_recent_gemini_eth_bid, most_recent_bitfinex_eth_ask, most_recent_bitfinex_eth_bid))
            f.write('\n')

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_korea_eth_ask", most_recent_korea_eth_ask, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_korea_eth_bid", most_recent_korea_eth_bid, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_korea_btc_ask", most_recent_korea_btc_ask, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_korea_btc_bid", most_recent_korea_btc_bid, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_gemini_eth_ask", most_recent_gemini_eth_ask, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_gemini_eth_bid", most_recent_gemini_eth_bid, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_bitfinex_eth_ask", most_recent_bitfinex_eth_ask, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.most_recent_bitfinex_eth_bid", most_recent_bitfinex_eth_bid, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        # BLUE: Sell BTC for KRW in Korea, buy ETH with KRA in Korea, transfer ETH to US, sell ETH in US for BTC
        krw = btcAmt * most_recent_korea_btc_bid * (1 - .000025)  # With coupons
        eth = krw / most_recent_korea_eth_ask * (1 - .000025)  # With coupons
        eth = eth - .01
        btc = most_recent_gemini_eth_bid * eth * (1 - .0015) # As a maker
        gain = btc - btcAmt
        
        # alias(
        #      scale(
        #         offset(
        #             scale(
        #                 multiplySeries(*.most_recent_gemini_eth_bid,
        #                     offset(
        #                         divideSeries(
        #                             scale(
        #                                 scale(
        #                                     timeShift(*.most_recent_korea_btc_bid, "-5min"), 2)
        #                             , 0.99975),
        #                             scale(timeShift(*.most_recent_korea_eth_ask, "-5min"), 0.99975)
        #                     ), -0.01)
        #                 ),
        #             0.9985),
        #          -2),
        #         4050
        #      ), "Buy Korea, sell US"
        # )

        with open("ticker.csv", "a") as f:
            output = "BLUES, %s, %s, $%s" % (timestamp, gain, gain * btcPrice)
            f.write(output)
            f.write('\n')
            print output
            
        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.BLUESbtc", gain, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.BLUESusd", gain * btcPrice, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]

        # RED: Buy ETH in US, sell ETH for KRW in Korea, buy BTC for KRW in Korea, transfer BTC to US, sell BTC in US for ETH
        eth = btcAmt / most_recent_gemini_eth_ask * (1 - .0015) # As a maker
        krw = eth * most_recent_korea_eth_bid  * (1 - .000025) # With coupons
        btc = krw / most_recent_korea_btc_ask * (1 - .000025) # With coupons
        btc = btc - .0005
        gain = btc - btcAmt
        with open("ticker.csv", "a") as f:
            output = "REDS, %s, %s, $%s" % (timestamp, gain, gain * btcPrice)
            f.write(output)
            f.write('\n')
            print output
            
        # alias(
        #     scale(
        #        offset(
        #            offset(
        #                divideSeries(
        #                        multiplySeries(
        #                                scale(scale(invert(timeShift(*.most_recent_gemini_eth_ask, "-5min")), 2), 0.9985),
        #                                scale(*.most_recent_korea_eth_bid, 0.99975)
        #                        ), scale(*.most_recent_korea_btc_ask, 0.99975)
        #                ), -0.0005),
        #             -2),
        #        4050
        #     ), "Buy US, Sell Korea"
        # )
            
        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.REDSbtc", gain, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
    
        cmd = "echo \"%s %s %s\" | nc 127.0.0.1 2003" % ("local.REDSusd", gain * btcPrice, timestamp)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
            
        time.sleep(10)
    except Exception as e:
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

"""