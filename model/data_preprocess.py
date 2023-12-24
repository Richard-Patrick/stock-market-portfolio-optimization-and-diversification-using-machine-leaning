import pandas as pd
class data_process():
    def clean():
        adj = pd.read_csv('Data/Stock_History/adj.csv')
        adj = adj.dropna(axis='columns')
        adj.to_csv('Data/Stock_History/adj.csv',index=False)

        close = pd.read_csv('Data/Stock_History/closing.csv')
        close = close.dropna(axis='columns')
        close.to_csv('Data/Stock_History/closing.csv',index=False)

        high = pd.read_csv('Data/Stock_History/high.csv')
        high = high.dropna(axis='columns')
        high.to_csv('Data/Stock_History/high.csv',index=False)

        low = pd.read_csv('Data/Stock_History/low.csv')
        low = low.dropna(axis='columns')
        low.to_csv('Data/Stock_History/low.csv',index=False)

        open = pd.read_csv('Data/Stock_History/opening.csv')
        open = open.dropna(axis='columns')
        open.to_csv('Data/Stock_History/opening.csv',index=False)

        open = pd.read_csv('Data/Stock_History/volume.csv')
        open = open.dropna(axis='columns')
        open.to_csv('Data/Stock_History/volume.csv',index=False)



