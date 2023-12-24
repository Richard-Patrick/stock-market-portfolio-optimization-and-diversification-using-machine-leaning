import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

class stock_diversify():
    def diversify():

        gics_sectors = [ 'XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLI', 'XLB', 'XLRE', 'XLK','XLU', 'XLV',]

        start_date = "2020-01-01"
        end_date = "2023-06-19"


        data = yf.download(gics_sectors, start=start_date, end=end_date, progress=False)

        returns = data['Adj Close'].pct_change().dropna()
        cumulative_returns = (1 + returns).cumprod()

        # Calculate growth percentages for each sector
        growth_percentages = {}
        for symbol in gics_sectors:
            sector_data = data['Adj Close'][symbol]
            growth_percentage = (sector_data[-1] - sector_data[0]) / sector_data[0] * 100
            growth_percentages[symbol] = growth_percentage
        
        # Initialize a dictionary to store the returns
        returns_dict = {}

        # Initialize a list to store the forecasted dataframes
        forecast_dfs = []

        data_close = data['Adj Close']
        
        data_close = data_close.reset_index(inplace=False)


        # Fetch historical stock price data and make predictions for each stock
        for symbol in gics_sectors:
    
            # Reset the index and keep only 'Date' and 'Close' columns
            stock_data = data_close[['Date', symbol]]
            stock_data.columns = ['ds', 'y']
            
            # Create and fit the Prophet model
            model = Prophet()
            model.fit(stock_data)

            # Generate future dates
            future_dates = model.make_future_dataframe(periods=365)

            # Make predictions
            forecast = model.predict(future_dates)

            # Extract the relevant columns from the forecast
            forecast_subset = forecast[['ds', 'yhat']]

            # Filter the forecast for next year's data
            next_year_forecast = forecast_subset[forecast_subset['ds'].dt.year == forecast_subset['ds'].dt.year.max()]

            # Calculate the percentage change in stock prices
            start_price = next_year_forecast.iloc[0]['yhat']
            end_price = next_year_forecast.iloc[-1]['yhat']
            returns = (end_price - start_price) / start_price * 100

            # Store the returns in the dictionary
            returns_dict[symbol] = returns

            # Store the forecast dataframe
            forecast_dfs.append(forecast_subset)
        
        result = {key: growth_percentages.get(key, 0) - returns_dict.get(key, 0) for key in set(growth_percentages) | set(returns_dict)}

        # diversity of stock using growth percentages
        # Calculate the sum of all values in the dictionary
        sum_values = sum(growth_percentages.values())
        # Calculate the percentage for each value
        percentages = {key:  round((value / sum_values) * 100,0) for key, value in growth_percentages.items()}

        new_keys = ['Communication Services','Consumer Discretionary','Consumer Staples','Energy','Financials','Industrials','Materials','Real Estate', 'Information Technology' ,'Utilities', 'Health Care']

        for i, old_key in enumerate(list(percentages.keys())):
            new_key = new_keys[i]
            percentages[new_key] = percentages.pop(old_key)
        
        return(percentages)

