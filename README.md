# Binance-Triangular-Arbitrage-Bot
Proof-of-concept Python3 Bot that looks for and trades Triangular Arbitrage on the [Binance Exchange](https://www.binance.com/?ref=25062167)

## Disclaimer:

### This bot is intended to be a Proof-of-concept. The developer will not be responsible for Any losses that are made are as a result of using this tool. Understand the risks involved and Only invest amounts you are willing to lose.  

## Supporting
If you appreciate my work send all crypto donations in Eth, Bnb, Matic, Avax etc on any chain to : 0xe0a09b49721FBD8B23c67a3a9fdE44be4412B8fD

## The theory

read a little about triangular arbitrage on [Investopedia](https://www.investopedia.com/terms/t/triangulararbitrage.asp)

## Requirements:
[Binance Account](https://www.binance.com/?ref=25062167)

## Required Libraries:
Python-Binance
Python3

## Usage:
Replace the values in api_key and api_secret in the ArbitrageMain.py file with your own keys generated via the Binance account console. Once this is done, simply run the ArbitrageMain file. To end the program, simple stop the python console.

## Customisation:

You can decide what percentage of your BTC value you want to trade by changing the portion value within the CoreFunctionality.py And ArbitrageMain.py files. Default value is 0.01 (1% of current available BTC Balance)

You can adjust the minimum amount of BNB to keep on hand by changing the minimumBnb value within CoreFunctionality.py. Default value is 0.03 BNB

You can adjust the minimum percentage to look for by changing the profits value in ArbitrageMain.py. Default value is 0.001 (triangles with 0.1% profit)

## Q and A:

### Does this make money?

No, it loses money extremely slowly due to hemorrhaging. Trades are executed via market trades, which are known to be worse then placing a limit order. Limit orders cannot be placed on binance when trading in extremely small amounts. The frequency of trading also means that the fees add up quickly. There might also be math errors in the calculations which cause false positives.
