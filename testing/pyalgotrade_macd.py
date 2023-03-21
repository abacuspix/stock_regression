from pyalgotrade import strategy
from pyalgotrade.technical import macd
from pyalgotrade.technical import cross
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades


class MacdStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, fastEMA, slowEMA, signalEMA):
        super().__init__(feed)
        self.__instrument = "NVDA"
        self.__macd = macd.MACD(feed[self.__instrument].getCloseDataSeries(), fastEMA, slowEMA, signalEMA)
        self.__position = None

    def onBars(self, bars):
        bar = bars[self.__instrument]

        # Check if MACD line crosses signal line
        if cross.cross_above(self.__macd.getHistogram(), self.__macd.getSignal()):
            # Buy signal
            if self.__position is None:
                self.__position = self.enterLong(self.__instrument, 100)
        elif cross.cross_below(self.__macd.getHistogram(), self.__macd.getSignal()):
            # Sell signal
            if self.__position is not None:
                self.__position.exitMarket()
                self.__position = None

def run_strategy():
    # Load Yahoo! Finance data feed
    instrument = "NVDA"
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, "data\\us\\NVDA.csv")

    # Create strategy and run it
    myStrategy = MacdStrategy(feed, 12, 26, 9)
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    myStrategy.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    myStrategy.attachAnalyzer(tradesAnalyzer)

    myStrategy.run()

    print("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult(),)
    print("累计回报率 Cumulative returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100),)
    print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)),)
    print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100),)
    print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))  

if __name__ == "__main__":
    run_strategy()