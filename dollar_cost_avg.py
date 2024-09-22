from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt



def main():
    msft = yf.Ticker("MSFT")
    hist = msft.history(period="10y")
    print(hist)

if __name__ == '__main__':
    main()
