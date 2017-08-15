import subprocess
from subprocess import call
with open("raw.csv", "r") as f:
    for line in f.readlines():
        line = line.split(", ")
        timestamp = line[0]
        most_recent_korea_eth_ask = line[1]

        cmd = "echo \"%s:%s|c\" | nc -w 1 -u 127.0.0.1 8125" % ("most_recent_korea_eth_ask", line[1])
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        break
        most_recent_korea_eth_bid = line[2]
        most_recent_korea_btc_ask = line[3] 
        most_recent_korea_btc_bid = line[4]
        most_recent_gemini_eth_ask = line[5]
        most_recent_gemini_eth_bid = line[6]
        most_recent_bitfinex_eth_ask = line[7]
        most_recent_bitfinex_eth_bid = line[8]

        


        