import model.stock_diversify as stock_diversify
import model.stock_optimizer as stock_optimizer
import model.KMeans_risk_reducing as risk_reducing
if __name__ == "__main__":
    diversify = stock_diversify.stock_diversify.diversify()
    risk_stock = risk_reducing.Kmeans_model.risk_reducing()
    stock_optimizer.stock_optimizer.optimize_stock(diversify,risk_stock)
    