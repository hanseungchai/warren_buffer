from pytrends.request import TrendReq


class GoogleIntern:
    def __init__(self):
        self.pytrends = TrendReq(retries=20, backoff_factor=0.1)
        self.trend_champion = ""

    def get_trends(self, ticker_list, company_list):
        batch = []
        contestants = []
        contestants_score = []
        winners = []
        for ticker in ticker_list:
            if ticker in ["ON", "IT", "PEAK", "FAST", "BIO", "A"]:
                i = ticker_list.index(ticker)
                batch.append(company_list[i])
            else:
                batch.append(ticker + " stock")

            if len(batch) > 4:
                self.pytrends.build_payload(batch, cat=0, timeframe='now 1-d', geo='US', gprop='')
                tournament_df = self.pytrends.interest_over_time()
                for com in batch:
                    contestants.append(com)
                    contestants_score.append(sum(tournament_df[com]))
                winners.append(contestants[contestants_score.index(max(contestants_score))])
                contestants = []
                contestants_score = []
                batch = []

        sec_winners = []
        for ticker in winners:
            batch.append(ticker)
            if len(batch) > 4:
                self.pytrends.build_payload(batch, cat=0, timeframe='now 1-d', geo='US', gprop='')
                tournament_df = self.pytrends.interest_over_time()
                for com in batch:
                    contestants.append(com)
                    contestants_score.append(sum(tournament_df[com]))
                sec_winners.append(contestants[contestants_score.index(max(contestants_score))])
                contestants = []
                contestants_score = []
                batch = []

        third_winners = []
        for ticker in sec_winners:
            batch.append(ticker)
            if len(batch) > 4:
                self.pytrends.build_payload(batch, cat=0, timeframe='now 1-d', geo='US', gprop='')
                tournament_df = self.pytrends.interest_over_time()
                for com in batch:
                    contestants.append(com)
                    contestants_score.append(sum(tournament_df[com]))
                third_winners.append(contestants[contestants_score.index(max(contestants_score))])
                contestants = []
                contestants_score = []
                batch = []

        champion = []
        for ticker in third_winners:
            batch.append(ticker)
            if len(batch) == 4:
                self.pytrends.build_payload(batch, cat=0, timeframe='now 1-d', geo='US', gprop='')
                tournament_df = self.pytrends.interest_over_time()
                for com in batch:
                    contestants.append(com)
                    contestants_score.append(sum(tournament_df[com]))
                champion.append(contestants[contestants_score.index(max(contestants_score))])
                contestants = []
                contestants_score = []
                batch = []

        self.trend_champion = champion[0]