from dual_sma_crossover import *
from pyalgotrade import plotter
#from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

logName="Google-dual-sma.log"

def run_strategy(smaPeriod1, smaPeriod2):
    # Load the bar feed from the CSV file

    instrument = "GOOGL"
    smaPeriod1 = smaPeriod1
    smaPeriod2 = smaPeriod2

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, "data\\us\\GOOGL.csv")
    #print(feeds)

    # Evaluate the strategy with the feed's bars.
    myStrategy = DualSMACrossOver(feed, instrument, smaPeriod1, smaPeriod2)
    # myStrategy.run()
    # # 打印总持仓：（cash + shares * price） （持有现金 + 股数*价格）
    #print(smaPeriod1, smaPeriod2, "Initial portfolio value: $%.2f" % myStrategy.getBroker().getEquity())
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    myStrategy.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    myStrategy.attachAnalyzer(tradesAnalyzer)

    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot(instrument).addDataSeries("SMA1", myStrategy.getSMA1())
    plt.getInstrumentSubplot(instrument).addDataSeries("SMA2", myStrategy.getSMA2())
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    # Run the strategy.
    myStrategy.run()

    """ print("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult())
    print("累计回报率 Cumulative returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100))
    print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
    print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))   """
    with open(logName, 'a') as f:
        f.write('\n')
        f.write("smaPeriod1 %f smaPeriod2 %f :" %(smaPeriod1, smaPeriod2),)
        f.write("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult(),)
        f.write("累计回报率 Cumulative returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100),)
        f.write("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)),)
        f.write("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100),)
        f.write("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))    
    # print("smaPeriod1 %f smaPeriod2 %f :" %(smaPeriod1, smaPeriod2),)
    # print("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult(),)
    # print("累计回报率 Cumulative returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100),)
    # print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)),)
    # print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100),)
    # print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))  
    # Plot the strategy.
    #plt.plot()
#run_strategy(5, 20)
for i in range(1,61):
    for j in range(1,251):
        if i<j:
            run_strategy(i, j)


