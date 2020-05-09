from pandas_datareader import data as pdr
from datetime import datetime
from datetime import timedelta
import yfinance as yf
yf.pdr_override()
import pandas as pd
from os import path
import calendar
import matplotlib.pyplot as plt

def ScrapeData(ticker, startdate, enddate):
    datafilename = ticker+'_'+startdate+'_'+enddate+'.csv'
    if path.exists(datafilename):
        print('{} exists'.format(datafilename))
    else:
        print('Scaping {} from {} to {}'.format(ticker, startdate, enddate))
        data = pdr.get_data_yahoo(ticker, start=startdate, end=enddate)
        data.to_csv(datafilename)
        print('Saved to {}'.format(datafilename))   

def GetData(ticker, startdate, enddate):
    datafilename = ticker+'_'+startdate+'_'+enddate+'.csv'
    if not path.exists(datafilename):
        ScrapeData(ticker, startdate, enddate)
    data = pd.read_csv(datafilename)
    return data

def BuyOnceWeekly(data, weekday):
    totalcost = 0.0
    totalshares = 0
    for date_str, closeprice in zip(data['Date'], data['Close']):
        oneday = datetime.strptime(date_str, '%Y-%m-%d').date()
        # 0 is Monday, 6 is Sunday
        if oneday.weekday() == weekday:
            totalcost += closeprice
            totalshares += 1
    print('Buy 1 share Every {}, {}, shares, Avg Cost, {:.2f}'.format(calendar.day_name[weekday], totalshares, totalcost/totalshares))

def BuyOnceDaily(data):
    totalcost = 0.0
    totalshares = 0
    for date_str, closeprice in zip(data['Date'], data['Close']):
        totalcost += closeprice
        totalshares += 1
    print('Buy 1 share Every day, {}, shares, Avg Cost, {:.2f}'.format(totalshares, totalcost/totalshares))
    #print('{}'.format(data.tail(1)))

def BuyOnceMonthly(data, targetdate):
    totalcost = 0.0
    totalshares = 0
    haspurchased = False
    first_day_of_month = datetime.strptime(data['Date'][0], '%Y-%m-%d').date()
    for date_str, closeprice in zip(data['Date'], data['Close']):
        oneday = datetime.strptime(date_str, '%Y-%m-%d').date()
        if oneday.year > first_day_of_month.year or oneday.month > first_day_of_month.month:
            first_day_of_month = oneday
            haspurchased = False
        if oneday - first_day_of_month >= timedelta(days=targetdate) and (not haspurchased):
            totalcost += closeprice
            totalshares += 1
            haspurchased = True
            #print('{} buy at {:.1f}'.format(oneday, closeprice))
    print('Buy 1 share Every Month {}st day, {}, shares, Avg Cost, {:.2f}'.format(targetdate, totalshares, totalcost/totalshares))
    
def BuyDip(data):
    totalcost = 0.0
    totalshares = 0
    yesterdayprice = data['Open'][0]
    for date_str, closeprice in zip(data['Date'], data['Close']):
        if closeprice < yesterdayprice*0.98:
            totalshares += 1
            totalcost += closeprice
        yesterdayprice = closeprice
    print('Buy 1 share Whenever a Dip, {} shares, Avg Cost: {:.2f}'.format(totalshares, totalcost/totalshares))

def plotData(data):
    plt.scatter(data['Date'][50:1000], data['Close'][50:1000], edgecolors='b')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price')
    plt.show()

def BuyBelowLastYearAvg(data):
    totalcost = 0.0
    totalshares = 0
    lastyearavg = 0.0
    lastyeartot = 0.0
    lastyeardaycnt = 0
    oneday = datetime.strptime(data['Date'][0], '%Y-%m-%d').date()
    last_year = oneday.year
    for date_str, closeprice in zip(data['Date'], data['Close']):
        oneday = datetime.strptime(date_str, '%Y-%m-%d').date()
        if oneday.year > last_year:
            lastyearavg = lastyeartot/lastyeardaycnt
            #print('{}: {:.2f}'.format(last_year, lastyearavg))
            lastyeartot = closeprice 
            lastyeardaycnt = 1            
        else:
            lastyeartot += closeprice
            lastyeardaycnt += 1
        if closeprice < 85:
            totalshares += 1
            totalcost += closeprice
            #print('{}: {:.1f} < {:.1f}'.format(oneday, closeprice, lastyearavg))
        last_year = oneday.year
    print('Buy 1 share Whenever lower last year avg, {} shares, Avg Cost: {:.2f}'.format(totalshares, totalcost/totalshares))

def main():
    #inception in year 1994
    ticker    = 'SPY'
    savingtime = 20
    for startyear in range(1994,2020 - savingtime):
        d1 = datetime(startyear, 1, 1)
        startdate = d1.strftime('%Y-%m-%d')
        d2 = datetime(startyear + savingtime, 12, 30)
        enddate   = d2.strftime('%Y-%m-%d')
        print('Study {} from {} to {}'.format(ticker, startdate, enddate))
        data = GetData(ticker, startdate, enddate)
        BuyOnceDaily(data)
        for i in range(0,5):
            BuyOnceWeekly(data, i)
        for i in range(1,24):
            BuyOnceMonthly(data, i)


if __name__ == '__main__':
    main()
        
        
