import yfinance as yf
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt

class Kmeans_model():
    def risk_reducing():
        df = pd.read_csv('Data/Stock_History/closing.csv')
        df = df.dropna(axis=1)
        df = df.drop('Date', axis=1)

        # Extract the closing prices
        closing_prices = df

        stock_symbols = list(df.columns.values)

        # Calculate risk metric (example: standard deviation of daily returns)
        risk_metric = closing_prices.pct_change().std()


        scaler = MinMaxScaler()
        normalized_risk = scaler.fit_transform(risk_metric.values.reshape(-1, 1))

        # Apply k-means clustering
        k = 3  # Number of clusters
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(normalized_risk)

        # Get the cluster labels for each stock
        cluster_labels = kmeans.labels_

        # Plot the clustering results
        plt.figure(figsize=(10, 6))
        colors = ['r', 'g', 'b']  # Colors for the clusters

        for i, label in enumerate(cluster_labels):
            plt.scatter(i, risk_metric[i], color=colors[label], alpha=0.7)

        # Highlight the high-risk stocks
        high_risk_stocks = [stock_symbols[i] for i, label in enumerate(cluster_labels) if label == 2]
        high_risk_indices = [i for i, label in enumerate(cluster_labels) if label == 2]
        
        return(high_risk_stocks)