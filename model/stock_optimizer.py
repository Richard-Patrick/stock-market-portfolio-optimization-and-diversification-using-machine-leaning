import pandas as pd
import pypfopt
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import HRPOpt
from pypfopt.efficient_frontier import EfficientCVaR

class stock_optimizer():
    def optimize_stock(divers,risk_stock):

        portfolio = pd.read_csv("data/Stock_History/closing.csv")
        print(portfolio.shape)
        portfolio = portfolio.drop(columns=risk_stock)
        print(portfolio.shape)
        company = pd.read_csv("data/Company_data.csv")
        company = company.loc[company['Symbol'].isin(portfolio.columns)]


        def Mean_Variance_Optimization(data,latest_prices,portfolio_value):
            
            Mean_Historical_Return = mean_historical_return(data)
            Covariance_Shrinkage = CovarianceShrinkage(data).ledoit_wolf()

            Efficient_Frontier = EfficientFrontier(Mean_Historical_Return, Covariance_Shrinkage)
            weights = Efficient_Frontier.max_sharpe()
            
            cleaned_weights = Efficient_Frontier.clean_weights()
            
            performance = Efficient_Frontier.portfolio_performance(verbose=False)
        
            Discrete_Allocation = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_value)
            
            allocation, leftover = Discrete_Allocation.greedy_portfolio()

            allocation={key: value for key, value in allocation.items() if value >= 0}
            
            latest_prices.loc[list(allocation.keys())]

            value=latest_prices.loc[list(allocation.keys())]*list(allocation.values())

            value[value > 0].sum()

            performance = list(performance)
            performance[0] = performance[0]*100
            performance[1] = performance[1]*100

            return(allocation,leftover,performance)

        def Hierarchical_Risk_parity(data,latest_prices,portfolio_value):
            
            returns = data.pct_change().dropna()

            hrp = HRPOpt(returns)
            hrp_weights = hrp.optimize()

            hrp.portfolio_performance(verbose=True)
            
            print(dict(hrp_weights))

            da_hrp = DiscreteAllocation(hrp_weights, latest_prices, total_portfolio_value=100000)
            
            allocation, leftover = da_hrp.greedy_portfolio() 
            
            print("Discrete allocation (HRP):", allocation)
            
            print("Funds remaining (HRP): ${:.2f}".format(leftover))


        total_portfolio_value=100000
        latest_prices = get_latest_prices(portfolio.iloc[:, 1:])



        for key, value in divers.items():
            divers[key] = total_portfolio_value/100*value

        allocation = []
        leftover = 0
        performance = []

        for key, value in divers.items():
            allo,leftover,perf = Mean_Variance_Optimization(portfolio[list(company[company['GICS Sector'] == key].Symbol)],
                               get_latest_prices(portfolio[list(company[company['GICS Sector'] == key].Symbol)]),
                               (value+leftover))
            allocation.extend(list(allo.items()))
            performance.extend([perf])    

        print('Leftover',leftover)
        result = [sum(elements) for elements in zip(*performance)]
        performance = [value / len(performance) for value in result]
        print('Expected annual return',performance[0],
              '\nAnnual volatility',performance[1],
              '\nSharpe Ratio',performance[2])
        print(allocation)



