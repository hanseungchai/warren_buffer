import pandas as pd
import pyEX


class TickerIntern:
    def __init__(self, filepath):
        raw_list = pd.read_excel(filepath)
        self.ticker = list(raw_list['Symbol'][:502])
        self.company = list(raw_list['Security'][:502])
        self.sector = list(raw_list['GICS Sector'][:502])
        self.raw_ticker_data = {}

    def get_stock_info(self, token):
        batch_symbols = []
        for ticker in self.ticker:
            batch_symbols.append(ticker)
            if len(batch_symbols) >= 100:
                px_batch = pyEX.batch(symbols=batch_symbols,
                                      fields='chart',
                                      token=token,
                                      range_="1d",
                                      format="json")

                batch_symbols = []
                self.raw_ticker_data.update(px_batch)


def fetch_the_times(token, ticker):
    px_batch_news = pyEX.batch(symbols=[ticker],
                               fields='news',
                               token=token,
                               range_="1d",
                               format="json")
    return px_batch_news