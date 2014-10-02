
import pandas.io.data as web
import pandas as pd
import matplotlib.pyplot as plt
#import jAnalysis as jana
import pylab
from matplotlib.ticker import MultipleLocator
from matplotlib.dates import DateFormatter
import datetime as dt

#reload(jana)

all_data={}

dateStart=dt.date(2003,1,1)
dateEnd=dt.date(2013,1,1)
dateRange=[dateStart + dt.timedelta(days=i) for i in range((dateEnd-dateStart).days)]


stockcodes=['AAPL', '2498.TW', '005935.KS']

for ticker in stockcodes:
    all_data[ticker]=web.get_data_yahoo(ticker, '1/1/2003', '1/1/2013')

price=pd.DataFrame({tic:data['Adj Close'] for tic, data in all_data.iteritems()}, index=dateRange)
#int(price['AAPL'])

data=pd.DataFrame(zip(list(price.index), list(price['AAPL'])), columns=['X', 'Y'])

price['005935.KS']=price['005935.KS']/1000

#----------------------------------------------------------------------

AAPL=pd.DataFrame(price['AAPL'], columns=['Y'])
AAPL['X']=AAPL.index

#rw=jana.RegWin(AAPL)
#start=0
#end=300

#sigs=rw.fullScan(minLen=500, maxLen=501, start=start, end=end, coverRate=0.5)
#rw.getSigPlots(sigs=sigs, sigsStart=0, sigsEnd=3, start=start, end=end)
'''
sigs=rw.fullScan(minLen=47, maxLen=50, start=start, end=end, coverRate=0.5)
rw.getSigPlots(sigs=sigs, sigsStart=0, sigsEnd=3, start=start, end=end)
'''
#sigs=rw.downward(minLen=10, maxLen=100, start=start, end=end, coverRate=0.5)
#rw.getSigPlots(sigs=sigs, sigsStart=0, sigsEnd=3, start=start, end=end)

#print(sigs)






