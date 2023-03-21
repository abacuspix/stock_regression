# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade import plotter
#from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import vwap
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
import pandas as pd
import zwQTBox as zwx


class VWAPMomentum(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, vwapWindowSize, threshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__vwap = vwap.VWAP(feed[instrument], vwapWindowSize)
        self.__threshold = threshold

    def getVWAP(self):
        return self.__vwap

    def onBars(self, bars):
        vwap = self.__vwap[-1]
        if vwap is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        price = bars[self.__instrument].getClose()
        notional = shares * price

        if price > vwap * (1 + self.__threshold) and notional < 1000000:
            self.marketOrder(self.__instrument, 100)
        elif price < vwap * (1 - self.__threshold) and notional > 0:
            self.marketOrder(self.__instrument, -100)


def main(plot):
    cod="NVDA";#万达院线
    cname='NVDA';
    fss="data\\us\\"+cod+".csv";
    df=pd.read_csv(fss,encoding='gbk');
    #df2=zwBox.zw_df2yhaoo(df);
    df2=zwx.df2yhaoo(df);
    cfn="dat\\"+cod+"_yh.csv";print(fss);
    df2.to_csv(cfn,encoding='utf-8')
    #
    #instrument = "aapl" #使用新变量名cname替代
    vwapWindowSize = 5
    threshold = 0.01

    # Download the bars.
    #feed = yahoofinance.build_feed([cname], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(cname,cfn)

    strat = VWAPMomentum(feed, cname, vwapWindowSize, threshold)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    retAnalyzer = returns.Returns()
    strat.attachAnalyzer(retAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(cname).addDataSeries("vwap", strat.getVWAP())

    strat.run()
    print("最终资产价值 Final portfolio value: $%.2f" % strat.getResult())
    print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
    print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

    if plot:
        plt.plot()

if __name__ == "__main__":
    main(True)
