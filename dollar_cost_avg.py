from pandas_datareader import data as pdr
from datetime import datetime
import yfinance as yf
yf.pdr_override()
import pandas as pd
from os import path
import calendar

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
    print('Buy 1 share Every {}, {} shares, Avg Cost: {:.2f}'.format(calendar.day_name[weekday], totalshares, totalcost/totalshares))

def BuyOnceDaily(data):
    totalcost = 0.0
    totalshares = 0
    for date_str, closeprice in zip(data['Date'], data['Close']):
        totalcost += closeprice
        totalshares += 1
    print('Buy 1 share Every day, {} shares, Avg Cost: {:.2f}'.format(totalshares, totalcost/totalshares))

def BuyOnceMonthly(data):
    totalcost_1st_day = 0.0
    totalshares = 0
    last_month = datetime.strptime(data['Date'][0], '%Y-%m-%d').date().month
    last_year = datetime.strptime(data['Date'][0], '%Y-%m-%d').date().year
    for date_str, closeprice in zip(data['Date'], data['Close']):
        oneday = datetime.strptime(date_str, '%Y-%m-%d').date()
        if oneday.year > last_year or oneday.month > last_month:
            totalcost_1st_day += closeprice
            totalshares += 1
        yesterdayprice = closeprice
        last_month = oneday.month
        last_year = oneday.year
    print('Buy 1 share Every Month 1st day, {} shares, Avg Cost: {:.2f}'.format(totalshares, totalcost_1st_day/totalshares))
            
def main():
    ticker    = 'SPY'
    for startyear in range(1980,1981):
        d1 = datetime(startyear, 1, 1)
        startdate = d1.strftime('%Y-%m-%d')
        d2 = datetime(startyear+20, 12, 30)
        enddate   = d2.strftime('%Y-%m-%d')
        print('Study {} from {} to {}'.format(ticker, startdate, enddate))
        data = GetData(ticker, startdate, enddate)
        for i in range(0,5):
            BuyOnceWeekly(data, i)
        BuyOnceDaily(data)
        BuyOnceMonthly(data)

if __name__ == '__main__':
    main()
        
        
