from pyalgotrade import strategy
from pyalgotrade import technical
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade import dataseries
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.utils import stats

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        
        # 创建收盘价、20天均线和250天均线的技术指标
        self.__priceDS = feed[instrument].getCloseDataSeries()
        self.__sma20 = ma.SMA(self.__priceDS, 20)
        self.__sma250 = ma.SMA(self.__priceDS, 120)
        
        # 创建RSI技术指标
        self.__rsi = rsi.RSI(self.__priceDS, 14)
        
    def onBars(self, bars):
        bar = bars[self.__instrument]
        
        # 如果收盘价大于250天均线，则使用20天均线策略
        if bar.getClose() > self.__sma250[-1]:
            if self.__sma20[-1] is None:
                return
            
            shares = self.getBroker().getCash() / bar.getClose()
            self.buy(self.__instrument, shares)
            
            # 如果当前持有头寸，则检查是否应该平仓
            if self.getBroker().getShares(self.__instrument) > 0 and self.__rsi[-1] >= 70:
                self.sell(self.__instrument, shares)
        
        # 如果收盘价小于等于250天均线，则使用RSI策略
        else:
            if self.__rsi[-1] is None:
                return
            
            shares = self.getBroker().getCash() / bar.getClose()
            
            # 如果RSI小于30，则买入
            if self.__rsi[-1] < 30:
                self.buy(self.__instrument, shares)
            
            # 如果当前持有头寸，则检查是否应该平仓
            elif self.getBroker().getShares(self.__instrument) > 0 and self.__rsi[-1] >= 70:
                self.sell(self.__instrument, shares)

# 设置数据源和交易品种
instrument='AAPL'
feed = yahoofeed.Feed()
feed.addBarsFromCSV(instrument, "data\\us\\TQQQ.csv")

# 初始化并运行策略
myStrategy = MyStrategy(feed, "AAPL")
myStrategy.run()

# 输出收益率、夏普比率等统计指标
retAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(retAnalyzer)

print("Final portfolio value: $%.2f" % myStrategy.getResult())
print("Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print("Sharpe ratio: %.2f" % (stats.getSharpeRatio(retAnalyzer.getCumulativeReturns()) ))
