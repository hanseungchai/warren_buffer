# IMPORTS
import os
import datetime as dt
import pandas as pd

import ticker_intern
import ticker_intern as ti
import calc_intern as ci
import google_intern as gi


# VAR
ticker_list_fp = "buffer_intel/wiki_stock_intel.xlsx"
iex_token_temp = os.environ["IEX_TOKEN"]


# GET TICKER/COMPANY (S&P 500) and STOCK DATA FROM IEX
TickerIntern = ti.TickerIntern(ticker_list_fp)
TickerIntern.get_stock_info(iex_token_temp)

# GET BASIC CALC STATS
CalcIntern = ci.CalcIntern()
CalcIntern.calculate_basic_stats(TickerIntern.raw_ticker_data, TickerIntern.sector)

# GET TRENDS DATA AND GET CHAMPION
GoogleIntern = gi.GoogleIntern()
GoogleIntern.get_trends(TickerIntern.ticker, TickerIntern.company)


# ------------- ANSWER THE QUESTIONS! ----------------- #
# MOST TRADED STOCK?
most_traded_ticker_value = max(CalcIntern.stock_trade_vol_acc)
i = CalcIntern.stock_trade_vol_acc.index(most_traded_ticker_value)
most_traded_ticker = CalcIntern.ticker_lst[i]

# MOST VOLATILE? (1m)
i = CalcIntern.comparative_vol.index(max(CalcIntern.comparative_vol))
most_volatile_ticker = CalcIntern.ticker_lst[i]
most_volatile_ticker_value = max(CalcIntern.price_vol_lst)

# BIGGEST LOSER?
biggest_ticker_loss_value = min(CalcIntern.price_movement_lst)
i = CalcIntern.price_movement_lst.index(biggest_ticker_loss_value)
biggest_loser_ticker = CalcIntern.ticker_lst[i]

# BIGGEST GAINER?
biggest_ticker_gain_value = max(CalcIntern.price_movement_lst)
i = CalcIntern.price_movement_lst.index(biggest_ticker_gain_value)
biggest_gainer_ticker = CalcIntern.ticker_lst[i]

# MOST TRADED SECTOR?
most_traded_sector = ""
most_volatile_sector = ""
most_loss_sector = ""
most_gain_sector = ""

most_traded_sector_value = 0
contesting_traded_sector_value = 0

most_volatile_sector_value = 0
most_volatile_sector_value_avg = 0
contesting_volatile_sector_value = 0

most_loss_sector_value = 100
contesting_loss_sector_value = 0

most_gain_sector_value = -100
contesting_gain_sector_value = 0

for key in list(CalcIntern.sector_stats.keys()):
    data = CalcIntern.sector_stats[key]
    contesting_traded_sector_value = sum(data["stock_trade_vol_acc"])
    contesting_volatile_sector_value = sum(data["comparative_vol"])/len(data["comparative_vol"])
    contesting_loss_sector_value = sum(data["price_movement"])/len(data["price_movement"])
    contesting_gain_sector_value = sum(data["price_movement"])/len(data["price_movement"])

    if contesting_traded_sector_value > most_traded_sector_value:
        most_traded_sector_value = contesting_traded_sector_value
        most_traded_sector = key

    if contesting_volatile_sector_value > most_volatile_sector_value:
        most_volatile_sector_value = contesting_volatile_sector_value
        most_volatile_sector_value_avg = sum(data["stock_price_vol"])/len(data["stock_price_vol"])
        most_volatile_sector = key

    if contesting_loss_sector_value < most_loss_sector_value:
        most_loss_sector_value = contesting_loss_sector_value
        most_loss_sector = key

    if contesting_gain_sector_value > most_gain_sector_value:
        most_gain_sector_value = contesting_gain_sector_value
        most_gain_sector = key


# MOST TOPICAL
most_searched = GoogleIntern.trend_champion
search_term = most_searched
news_soup = ""
if " stock" in search_term:
    news = ticker_intern.fetch_the_times(iex_token_temp, search_term.strip(" stock"))['news']
    if len(news) > 5:
        news = news[:5]

    if len(news):
        for ppr in news:
            news_str = f"{ppr['source']}: {ppr['headline']} \n[{ppr['url']}]\n"
            news_soup += news_str
    else:
        news_soup = "Unfortunately, I got nothing!"

else:
    i = TickerIntern.company.index(search_term)
    news = ticker_intern.fetch_the_times(iex_token_temp, TickerIntern.ticker[i])['news']
    if len(news) > 5:
        news = news[:5]

    if len(news):
        for ppr in news:
            news_str = f"{ppr['source']}:\t\t {ppr['headline']} \n[{ppr['url']}]\n"
            news_soup += news_str
    else:
        news_soup = "Unfortunately, I got nothing!"


# ORGANIZE AND XL
time_date = dt.datetime.today()

buffer_records_df = pd.read_excel("buffer_intel/wisdoms_from_buffer.xlsx")
export_line = [time_date, most_traded_ticker, most_traded_ticker_value, most_volatile_ticker,
               most_volatile_ticker_value, biggest_loser_ticker, biggest_ticker_loss_value, biggest_gainer_ticker,
               biggest_ticker_gain_value, most_traded_sector, most_traded_sector_value, most_volatile_sector,
               most_volatile_sector_value_avg, most_loss_sector, most_loss_sector_value, most_gain_sector,
               most_gain_sector_value, most_searched, news_soup]

biggest_ticker_loss_value = str('%.2f' % biggest_ticker_loss_value)+"%"
biggest_ticker_gain_value = str('%.2f' % biggest_ticker_gain_value)+"%"
most_loss_sector_value = str('%.2f' % most_loss_sector_value)+"%"
most_gain_sector_value = str('%.2f' % most_gain_sector_value)+"%"

if "-" in biggest_ticker_loss_value:
    biggest_ticker_loss_value = biggest_ticker_loss_value.replace("-", "▼ ")
else:
    biggest_ticker_loss_value = "▲ " + biggest_ticker_loss_value

if "-" in biggest_ticker_gain_value:
    biggest_ticker_gain_value = biggest_ticker_gain_value.replace("-", "▼ ")
else:
    biggest_ticker_gain_value = "▲ " + biggest_ticker_gain_value

if "-" in most_loss_sector_value:
    most_loss_sector_value = most_loss_sector_value.replace("-", "▼ ")
else:
    most_loss_sector_value = "▲ " + most_loss_sector_value

if "-" in most_gain_sector_value:
    most_gain_sector_value = most_gain_sector_value.replace("-", "▼ ")
else:
    most_gain_sector_value = "▲ " + most_gain_sector_value


print(f'\n[{str(time_date).split(" ")[0]}]')
print(f"You seek the wisdom of Warren Buffer\n\n")
print(f"[TICKERS DATA]")
print(f"Highest Trade Volume:\t {most_traded_ticker}\t{most_traded_ticker_value}")
print(f"Most Volatile:\t\t\t {most_volatile_ticker}\t"f"{'%.2f' % most_volatile_ticker_value}")
print(f"Biggest loser:\t\t\t {biggest_loser_ticker}\t{biggest_ticker_loss_value}")
print(f"Biggest gainer:\t\t\t {biggest_gainer_ticker}\t{biggest_ticker_gain_value}\n")
print(f"[SECTOR DATA]")
print(f"Highest Trade Volume:\t {most_traded_sector}\t{most_traded_sector_value}")
print(f"Most Volatile:\t\t\t {most_volatile_sector}\t"f"{'%.2f' % most_volatile_sector_value_avg}")
print(f"Biggest loser:\t\t\t {most_loss_sector}\t{most_loss_sector_value}")
print(f"Biggest gainer:\t\t\t {most_gain_sector}\t{most_gain_sector_value}\n")
print(f"Warren has kindly visited the news vendor and hands you these papers.")
print(news_soup)
print(f"Lastly, Warren pulls out a ledger and writes down his wisdoms.\n")

buffer_records_df.loc[len(buffer_records_df), :] = export_line
buffer_records_df.to_excel("buffer_intel/wisdoms_from_buffer.xlsx", index=False)
