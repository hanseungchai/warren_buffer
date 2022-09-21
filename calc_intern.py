class CalcIntern:
    def __init__(self):
        self.basic_stats = {}
        self.ticker_lst = []
        self.price_mean_lst = []
        self.price_vol_lst = []
        self.comparative_vol = []
        self.price_movement_lst = []
        self.stock_trade_vol_acc = []
        self.sector_stats = {}

    def calculate_basic_stats(self, ticker_data, sector_lst):
        keys_lst = list(ticker_data.keys())

        for key in keys_lst:
            self.basic_stats[key] = {}
            stock_data_points = ticker_data[key]['chart']
            stock_trade_vol_acc = 0
            stock_price_lst = []
            for data in stock_data_points:
                if type(data['numberOfTrades']) == int:
                    stock_price_lst.append(data['average'])
                    stock_trade_vol_acc += data['numberOfTrades']

            price_mean = sum(stock_price_lst) / len(stock_price_lst)
            price_variance = sum([((x - price_mean) ** 2) for x in stock_price_lst]) / len(stock_price_lst)
            stock_price_vol = price_variance ** 0.5
            price_movement = (stock_price_lst[-1] - stock_price_lst[0]) * 100 / stock_price_lst[0]

            self.basic_stats[key]['price_mean'] = price_mean
            self.basic_stats[key]['stock_price_vol'] = stock_price_vol
            self.basic_stats[key]['price_movement'] = price_movement
            self.basic_stats[key]['stock_trade_vol_acc'] = stock_trade_vol_acc

        for key in list(self.basic_stats.keys()):
            self.ticker_lst.append(key)
            self.price_mean_lst.append(self.basic_stats[key]['price_mean'])
            self.price_vol_lst.append(self.basic_stats[key]['stock_price_vol'])
            self.comparative_vol.append(
                self.basic_stats[key]['stock_price_vol'] * 100 / self.basic_stats[key]['price_mean'])
            self.price_movement_lst.append(self.basic_stats[key]['price_movement'])
            self.stock_trade_vol_acc.append(self.basic_stats[key]['stock_trade_vol_acc'])

        sec_category = []
        for sec in sector_lst:
            if sec not in sec_category:
                sec_category.append(sec)
                self.sector_stats[sec] = {}
                self.sector_stats[sec]['stock_price_vol'] = []
                self.sector_stats[sec]['comparative_vol'] = []
                self.sector_stats[sec]['price_movement'] = []
                self.sector_stats[sec]['stock_trade_vol_acc'] = []

        for key in keys_lst:
            i = keys_lst.index(key)
            key_sec = sector_lst[i]
            self.sector_stats[key_sec]['stock_price_vol'].append(self.basic_stats[key]['stock_price_vol'])
            self.sector_stats[key_sec]['comparative_vol'].append(self.basic_stats[key]['stock_price_vol'] * 100 /
                                                                 self.basic_stats[key]['price_mean'])
            self.sector_stats[key_sec]['price_movement'].append(self.basic_stats[key]['price_movement'])
            self.sector_stats[key_sec]['stock_trade_vol_acc'].append(self.basic_stats[key]['stock_trade_vol_acc'])