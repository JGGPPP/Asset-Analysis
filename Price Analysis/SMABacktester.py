import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from datetime import date, timedelta

class SMABacktester():
    def __init__(self, asset, SMA_S, SMA_L,start,end):
        self.asset=asset
        self.SMA_S=SMA_S
        self.SMA_L=SMA_L
        self.start=start
        self.end=end
        self.results=None
        self.get_data()

    def get_data(self):
        df=yf.download(self.asset,self.start,self.end)
        data=pd.DataFrame(df.Close)
        data["returns"]=np.log(data.Close.div(data.Close.shift(1)))
        data["SMA_S"]=data.Close.rolling(self.SMA_S).mean() 
        data["SMA_L"]=data.Close.rolling(self.SMA_L).mean()
        data.dropna(inplace=True)
        self.data2=data

        return data

    def test_results(self):
        data=self.data2.copy().dropna()
        data["position"]=np.where(data["SMA_S"]>data["SMA_L"],1,-1)
        data["strategy"]=data["returns"]*data.position.shift(1)
        data.dropna(inplace=True)
        data["returnsbh"]=data["returns"].cumsum().apply(np.exp)
        data["returnsstrategy"]=data["strategy"].cumsum().apply(np.exp)
        performance=data["returnsstrategy"].iloc[-1]
        outperformance=performance-data["returnsbh"].iloc[-1]
        self.results=data

        ret= np.exp(data["strategy"].sum())
        std= data["strategy"].std()*np.sqrt(365)

        return print(f"Strategy return is {round(performance,6)}, which outperformed the Buy and Hold strategy by {round(outperformance,6)}")
    
    def plot_results(self):
        if self.results is None:
            print("Run the test please")
        else:
            title="{}| SMA_S={} | SMA_L{}".format(self.asset, self.SMA_S, self.SMA_L)
            self.results[["returnsbh","returnsstrategy"]].plot(title=title,figsize=(12,8))