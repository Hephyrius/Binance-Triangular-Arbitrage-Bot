# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 03:53:20 2018

@author: Khera
"""
import time
import binance
from binance.client import Client
from binance.enums import *

portion = 0.01
minimumBnb = 0.03

def getMarketData(client, exclude):
    
    tickers = client.get_orderbook_tickers()
    
    for i in tickers:
        
        if 'ETH' in i['symbol']:
            if i['symbol'].index('ETH') != 0:
                i['symbol'] = i['symbol'].replace('ETH','-ETH')
                
        if 'BTC' in i['symbol']:
            if i['symbol'].index('BTC') != 0:
                i['symbol'] = i['symbol'].replace('BTC','-BTC')
        
        if 'BNB' in i['symbol']:
            if i['symbol'].index('BNB') != 0:
                i['symbol'] = i['symbol'].replace('BNB','-BNB')
        
        if 'USDT' in i['symbol']:
            if i['symbol'].index('USDT') != 0:
                i['symbol'] = i['symbol'].replace('USDT','-USDT')
        
    for i in tickers:
        if '-' not in i['symbol']:
            if 'ETH' in i['symbol']:
                if i['symbol'].index('ETH') != 0:
                    i['symbol'] = i['symbol'].replace('ETH','-ETH')
                    
            if 'BTC' in i['symbol']:
                if i['symbol'].index('BTC') != 0:
                    i['symbol'] = i['symbol'].replace('BTC','-BTC')
            
            if 'BNB' in i['symbol']:
                if i['symbol'].index('BNB') != 0:
                    i['symbol'] = i['symbol'].replace('BNB','-BNB')
            
            if 'USDT' in i['symbol']:
                if i['symbol'].index('USDT') != 0:
                    i['symbol'] = i['symbol'].replace('USDT','-USDT')
                    
    for i in tickers:
        
        if '123456' in i['symbol']:
            tickers.remove(i)
        
        if 'RPX' in i['symbol']:
            tickers.remove(i)
        
        if 'VEN' in i['symbol']:
            tickers.remove(i)
        
        if 'HSR' in i['symbol']:
            tickers.remove(i)
#        if exclude == True:
#            if 'BNB' in i['symbol']:
#                tickers.remove(i)
    
    
    return tickers

def threeCurrencyArb(tickers, minimumPercentage, startingBal):
    
    btc = []
    found = False
    for i in tickers:
        
#        if 'ETH' in i['symbol']:
#            eth.append(i)
            
        if 'BTC' in i['symbol']:
            btc.append(i)    
            
#        if 'BNB' in i['symbol']:
#            bnb.append(i)
#            
#        if 'USDT' in i['symbol']:
#            usdt.append(i)        
            
    currencies = [btc]
    starting = startingBal
    results = []
    for i in currencies:
        marker1 = ""
        if i == 0:
            marker1 = "BTC"
        elif i == 1:
            marker1 = "ETH"
        elif i == 2:
            marker1 = "BNB"
        elif i == 3:
            marker1 = "USDT"
        
        for j in i:
            jmarker = j['symbol'].split('-')
            ask1 = j['askPrice']
            ask1qty = j['askQty']
            bid1 = j['bidPrice']
            
            for k in tickers:
                
                kmarker = k['symbol'].split('-')
                
                if kmarker[0] == jmarker[0] and kmarker[1] != jmarker[1] and found == False:
                    
                    ask2 = k['askPrice']
                    bid2 = k['bidPrice']
                    bid2qty = k['bidQty']
                
                    for l in tickers:
                        
                        lmarker = l['symbol'].split('-')
                        ask3 = l['askPrice']
                        bid3 = l['bidPrice']
                        bid3qty = l['bidQty']
                        
                        if lmarker[0] == kmarker[1] and lmarker[1] == jmarker[1] and found == False:
                            
                           
                            
                            step1 = (starting*0.999)/float(ask1)
                            step2 = (step1*0.999)*float(bid2)
                            step3 = (step2*0.999)*float(bid3)
                            
                            profitloss = (step3-starting)/starting
                            if profitloss > minimumPercentage:
                                percentageGain = (profitloss)*100
                                found = True
                                trade1 = [j['symbol'],ask1,bid1]
                                trade2 = [k['symbol'],ask2,bid2]
                                trade3 = [l['symbol'],ask3,bid3]
                                trade4 = ['NONE',0,0]
                                PL = [profitloss]
                                output= [trade1,trade2,trade3,trade4,PL]
                                results.append(output)
                                #print("Route: " + j['symbol'] +' -> '+  k['symbol'] + ' -> '+ l['symbol'] + ' has profit/loss of ' + str(percentageGain) +"%")
    return results

def checkOpenOrders(client, market):
    market = market.replace("-","")
    orders = client.get_open_orders(symbol=market)
    return orders
    
def getCoinBalance(client, currency):
    balance = float(client.get_asset_balance(asset=currency)['free'])
    return balance


def checkIntMarket(client, market):
    info = client.get_symbol_info(market)
    isInt = False
    intmarket = info['filters'][1]['stepSize'] 
    if float(intmarket) == 1:
        isInt = True
    elif intmarket !=1:
        isInt = False
    return isInt
        
def checkstep(client, market):
    info = client.get_symbol_info(market)
    stepSize = info['filters'][1]['stepSize'] 
    return stepSize


def executeTrade(client, market, currentAsset, tradeType, tradePrice, firstTrade):
    
    tradeMarket = market.replace("-","")
    
    intmarket = checkIntMarket(client,tradeMarket)
    
    balance = getCoinBalance(client, currentAsset)

    if firstTrade == True:
        balance = balance/portion
        
    if tradeType == 0:#sell
        if currentAsset == 'BNB':
                qtySell = balance - minimumBnb
        else:
            qtySell = balance
        
        if intmarket == True:
            qtySell = int(qtySell)
            
        elif currentAsset == 'ETH':
            
            qtySell2 = float("%.3f" % qtySell)
            
            if qtySell2>qtySell:
                
                qtySell = "%.3f" % (float(qtySell)-0.0005)
                
            else:
                
                qtySell = "%.3f" % qtySell
                
        else:
            
            qtySell = "%.2f" % qtySell
            
        order = client.order_market_sell(symbol=tradeMarket, quantity=qtySell)
        
    if tradeType == 1:# buy
        
        qtyBuy = balance/tradePrice
        
        if intmarket == True:
            qtyBuy = int(qtyBuy)
        else:
            qtyBuy = "%.2f" % qtyBuy

        order = client.order_market_buy(symbol=tradeMarket,quantity=qtyBuy)




