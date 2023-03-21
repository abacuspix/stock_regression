from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
import talib
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.utils import stats
import numpy as np


class KDJStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument

        # Use adjusted close values instead of close values
        self.setUseAdjustedValues(True)
       feed[instrument].dropna()
        # Convert SequenceDataSeries to numpy arrays
        high = np.asarray(feed[instrument].getHighDataSeries())
        low = np.asarray(feed[instrument].getLowDataSeries())
        close = np.asarray(feed[instrument].getAdjCloseDataSeries())

        # Calculate KDJ indicator
        self.__kdj_k, self.__kdj_d = talib.STOCH(high, low, close, 9, 3, 0, 3, 0)

    def onBars(self, bars):
        bar = bars[self.__instrument]

        if self.getBroker().getShares(self.__instrument) == 0:
            if self.__kdj_k[-1] > self.__kdj_d[-1] and self.__kdj_k[-2] <= self.__kdj_d[-2]:
                shares = int(self.getBroker().getCash() / bar.getAdjClose())
                self.buy(self.__instrument, shares)
        else:
            if self.__kdj_k[-1] < self.__kdj_d[-1] and self.__kdj_k[-2] >= self.__kdj_d[-2]:
                shares = self.getBroker().getShares(self.__instrument)
                self.sell(self.__instrument, shares)



# Load the yahoo feed from the CSV file
feed = yahoofeed.Feed()
feed.addBarsFromCSV("nvda", "data\\us\\nvda.csv")

# Initialize and run the strategy
myStrategy = KDJStrategy(feed, "nvda")
myStrategy.run()

# Print the results
retAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(retAnalyzer)

print("Final portfolio value: $%.2f" % myStrategy.getResult())
print("Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print("Sharpe ratio: %.2f" % (stats.getSharpeRatio(retAnalyzer.getCumulativeReturns())))
