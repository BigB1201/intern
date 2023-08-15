from sys import displayhook
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

BTC_Ticker = yf.Ticker("BTC-USD") 
BTC_Data = BTC_Ticker.history(period="1d")

print(BTC_Data)

file = open("bitcoin.csv", "w")
file.write(str(BTC_Data)) 

data = pd.read_csv("bitcoin.csv", encoding='latin1')
displayhook(data.head())   