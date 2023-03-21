# -*- coding: utf-8 -*-
import sma_crossover
from pyalgotrade import plotter
#from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
import pandas as pd
import zwQTBox as zwx


def main(plot):
    #--------数据格式转换，常用国内A股数据，转换为yahoo财经格式
    code="NVDA";#万达院线
    cname='NVDA';
    fss="data\\us\\"+code+".csv";
    df=pd.read_csv(fss,encoding='gbk');
    df2=zwx.df2yhaoo(df);
    cfn="data\\us"+code+"_yh.csv";print(fss);
    df2.to_csv(cfn,encoding='utf-8')
    #------------
    #instrument = "aapl",使用新变量名cname替代
    #smaPeriod = 163
    smaPeriod = 120

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(cname,cfn)


    strat = sma_crossover.SMACrossOver(feed,cname, smaPeriod)
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
        plt.getInstrumentSubplot(cname).addDataSeries("sma", strat.getSMA())

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
