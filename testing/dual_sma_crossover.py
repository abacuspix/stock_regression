import pyalgotrade
from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns

def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value

class DualSMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod1, smaPeriod2):
        super(DualSMACrossOver, self).__init__(feed, 100000)
        self.__position = None
        self.__instrument = instrument
        # # We'll use adjusted close values instead of regular close values.
        # self.setUseAdjustedValues(True)
        self.__sma1 = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod1)
        self.__sma2 = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod2)

    def getSMA1(self):
        return self.__sma1

    def getSMA2(self):
        return self.__sma2

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        #self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        #self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma2[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            #短期均价>长期均价 买入
            if self.__sma1[-1] > self.__sma2[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 100, True)
        # 短期均价<长期均价卖出
        elif self.__sma1[-1] < self.__sma2[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


