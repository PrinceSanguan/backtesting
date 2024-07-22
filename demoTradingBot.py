import datetime as dt
import yfinance as yf
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class MyMACDStrategy(Strategy):
    def init(self):
        price = self.data.Close
        macd, macd_signal, _ = talib.MACD(price)
        self.macd = self.I(lambda x: macd, price)
        self.macd_signal = self.I(lambda x: macd_signal, price)

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()

start = dt.datetime(2022, 1, 1)
end = dt.datetime(2024, 1, 1)
data = yf.download("AAPL", start=start, end=end)

backtest = Backtest(data, MyMACDStrategy, commission=.002, exclusive_orders=True)

print(backtest.run())

backtest.plot()
