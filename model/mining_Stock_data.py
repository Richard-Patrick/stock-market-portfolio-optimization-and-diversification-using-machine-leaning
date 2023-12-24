import pandas as pd
import matplotlib
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime

class Stock_data():
    def get_data():        
        df=pd.read_csv('Data/Company_data.csv')

        start_date = datetime(2020,1,1)
        end_date = datetime(2022,12,31)


        yf.pdr_override()

        y_symbols = df.Symbol.tolist()

        data = pdr.get_data_yahoo(y_symbols, start=start_date, end=end_date)

        data['Open'].to_csv('Data/Stock_History/opening.csv', index=True)
        data['High'].to_csv('Data/Stock_History/high.csv', index=True)
        data['Low'].to_csv('Data/Stock_History/low.csv', index=True)
        data['Close'].to_csv('Data/Stock_History/closing.csv', index=True)
        data['Adj Close'].to_csv('Data/Stock_History/adj.csv', index=True)
        data['Volume'].to_csv('Data/Stock_History/volume.csv', index=True)

        data.to_csv('Data/Stock_History.csv')


