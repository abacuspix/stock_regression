import sma_crossoverx
from pyalgotrade import plotter
#from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

logName="tqqq-report-SMA.log"
def main(plot):
    
    for smaPeriod in range(1,300):
        instrument = "tqqq"
        
    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
        feed = yahoofeed.Feed()
        feed.addBarsFromCSV(instrument, "data\\us\\tqqq.csv")


        strat = sma_crossoverx.SMACrossOver(feed, instrument, smaPeriod)
        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        strat.attachAnalyzer(sharpeRatioAnalyzer)
        retAnalyzer = returns.Returns()
        strat.attachAnalyzer(retAnalyzer)
        drawDownAnalyzer = drawdown.DrawDown()
        strat.attachAnalyzer(drawDownAnalyzer)
        tradesAnalyzer = trades.Trades()
        strat.attachAnalyzer(tradesAnalyzer)

        if plot:
            plt = plotter.StrategyPlotter(strat, False, True, True)
            plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())

        strat.run()
        with open(logName, 'a') as f:
            f.write('\n')
            f.write("smaPeriod value: %.2f" % smaPeriod,)
            f.write("最终资产价值 Final portfolio value: $%.2f" % strat.getResult(),)
            f.write("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100),)
            f.write("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)),)
            f.write("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100),)
            f.write("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))    

    #if plot:
    #    plt.plot()



if __name__ == "__main__":
    main(True)
