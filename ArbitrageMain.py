# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 03:53:20 2018

@author: Khera
"""

import time
from binance.client import Client
import CoreFunctionality as core

api_key = 'api_key'
api_secret = 'api_secret'
client = Client(api_key, api_secret)
btcHistory = []
profits = 0.001
mode = 0
previousMode = 0
portion = 0.01


tradeRoute = []
startingBalance = core.getCoinBalance(client, 'BTC')
startingBalanceEth = core.getCoinBalance(client, 'ETH')
startingBalanceBNB = core.getCoinBalance(client, 'BNB')
btcHistory.append(startingBalance)
startingBalance = startingBalance/portion
currentAsset = 'BTC'

while (mode <7):
    
    if mode == 0:
        print("Finding Arbitrage Opportunities")
        data = core.getMarketData(client, True)
        
        found = False
        
        tradeRoute = core.threeCurrencyArb(data,profits,startingBalance)
        if len(tradeRoute) > 0:
            print("Trade Found")
            found = True
            mode=1
        
    elif mode == 1:
        try:
            print("Executing Step 1 of trade")
            market = tradeRoute[0][0][0]
            tradeType = 1
            tradePrice = float(tradeRoute[0][0][1])
            core.executeTrade(client,market, currentAsset, tradeType, tradePrice, True)
            currentAsset = tradeRoute[0][0][0].split('-')[0]
            mode = 2
        except Exception as e:
            print(e)
            mode=0
        
    elif mode == 2:
        try:
            print("Executing Step2 of trade")
            market = tradeRoute[0][1][0]
            tradeType = 0
            tradePrice = float(tradeRoute[0][1][2])
            core.executeTrade(client,market, currentAsset, tradeType, tradePrice, False)
            currentAsset = tradeRoute[0][1][0].split('-')[1]
            mode=3
        except Exception as e:
            print(e)
            mode=0
        
        
    elif mode == 3:
        try:
            print("Executing Step3 of trade")
            market = tradeRoute[0][2][0]
            tradeType = 0
            tradePrice = float(tradeRoute[0][2][2])
            currBnb = float(core.getCoinBalance(client, 'BNB'))
            core.executeTrade(client,market, currentAsset, tradeType, tradePrice, False)
            currentAsset = tradeRoute[0][2][0].split('-')[1]
            mode = 5 
        except Exception as e:
            print(e)
            mode=0
            
    elif mode == 5:
        try:
            print("Calculating profit and Exiting")
            endBalance = core.getCoinBalance(client, 'BTC')/portion
            pl = (endBalance/startingBalance)
            startingBalance = core.getCoinBalance(client, 'BTC')
            btcHistory.append(startingBalance)
            startingBalance = startingBalance/portion
            
            
            endEthBalance = core.getCoinBalance(client, 'ETH')
            ethchange = (endEthBalance/startingBalanceEth)
            startingBalanceEth = core.getCoinBalance(client, 'ETH')
            
            endingBNB = core.getCoinBalance(client, 'BNB')
            bnbchange = (endingBNB/startingBalanceBNB)
            startingBalanceBNB = core.getCoinBalance(client, 'BNB')
            
            overallchange = (startingBalance*portion/btcHistory[0]) 
            
            expected = tradeRoute[0][4][0]
            route = "" + str(tradeRoute[0][0][0])+" -> " + str(tradeRoute[0][1][0])+" -> " + str(tradeRoute[0][2][0])
            print("Btc: " + str(pl) + " Eth: " + str(ethchange) +" Bnb: " + str(bnbchange) + " Net: " + str(overallchange) +" Route: " + route)
            mode = 0
        except Exception as e:
            print(e)
            mode=0

    else:
        mode == 666

btcstart = btcHistory[0]
btcEnd = btcHistory[len(btcHistory)-1]
ration = (btcEnd-btcstart/btcstart)*portion

print(ration)
#%%

#step = core.checkstep(client, 'BNBBTC')
    
    
    
    
    
    
    
    
    
    
    
    