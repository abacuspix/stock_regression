import rsi2
from pyalgotrade import plotter
#from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades


def main(plot):
    instrument = "SQQQ"
    entrySMA = 250
    exitSMA = 5
    rsiPeriod = 2
    overBoughtThreshold = 90
    overSoldThreshold = 10

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2009, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, "data\\us\\SQQQ.csv")

    strat = rsi2.RSI2(feed, instrument, entrySMA, exitSMA,
                      rsiPeriod, overBoughtThreshold, overSoldThreshold)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    retAnalyzer = returns.Returns()
    strat.attachAnalyzer(retAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, True, True)
        plt.getInstrumentSubplot(instrument).addDataSeries(
            "Entry SMA", strat.getEntrySMA())
        plt.getInstrumentSubplot(instrument).addDataSeries(
            "Exit SMA", strat.getExitSMA())
        plt.getOrCreateSubplot("rsi").addDataSeries("RSI", strat.getRSI())
        plt.getOrCreateSubplot("rsi").addLine(
            "Overbought", overBoughtThreshold)
        plt.getOrCreateSubplot("rsi").addLine("Oversold", overSoldThreshold)

    strat.run()
    print("最终资产价值 Final portfolio value: $%.2f" % strat.getResult())
    print("累计回报率 Cumulative returns: %.2f %%" %
          (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("夏普比率 Sharpe ratio: %.2f" %
          (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("最大回撤率 Max. drawdown: %.2f %%" %
          (drawDownAnalyzer.getMaxDrawDown() * 100))
    #print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))
    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
