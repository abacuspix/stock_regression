import sma_crossover
from pyalgotrade import plotter
#from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
from datetime import datetime
from tslib import *
import csv,os


def run_strategy(instrument, smaPeriod):
    instrument = instrument
    smaPeriod = smaPeriod

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    print ("data\\"+instrument+".csv")
    size = os.path.getsize("data\\us\\"+instrument+".csv")
    print (instrument,size)
    if size>200:
        feed.addBarsFromCSV(instrument, "data\\us\\"+instrument+".csv")
        strat = sma_crossover.SMACrossOver(feed, instrument, smaPeriod)
        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        strat.attachAnalyzer(sharpeRatioAnalyzer)
        retAnalyzer = returns.Returns()
        strat.attachAnalyzer(retAnalyzer)
        drawDownAnalyzer = drawdown.DrawDown()
        strat.attachAnalyzer(drawDownAnalyzer)
        tradesAnalyzer = trades.Trades()
        strat.attachAnalyzer(tradesAnalyzer)  
        strat.run()
        print("Instrument: %s" % instrument)
        print("最终资产价值 Final portfolio value: $%.2f" % strat.getResult())
        print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
        print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
        print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
        print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))
    else:
        pass
   

 

start = datetime.now()
print (start)
def getCodeFromYahooList():
    with open('c:\\stock\\inxYahoo.csv', 'r') as file:
        reader = csv.reader(file)
        stockList=[]
        for row in reader:
            stockList.append(row[0])
    return stockList

stockList=getCodeFromYahooList()
for codename in stockList:
    run_strategy(codename, 10)
