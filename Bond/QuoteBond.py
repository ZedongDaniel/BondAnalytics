import pandas as pd
from pandas.tseries.offsets import DateOffset
from Bond.BaseBond import BondAbstract
        
class Bond(BondAbstract):
    def __init__(self, quote) -> None:
        line = quote.split(",")
        self.coupon = float(line[3]) / 2
        self.maturity = pd.to_datetime(str(line[4]))
        self.next_coupon_date = pd.to_datetime(str(line[5]))
        self.num_coupon = int(line[6])
        self.identifier = str(line[10])
        self.ask_price = float(line[12])
        self.today = pd.to_datetime("2023/9/05")
        self.face_value = 100

        self.exact_date_ls, self.time_ls = self._calc_time_ls()
        self.coupon_ls = self._calc_coupon_ls()
        self.coupon_dic = dict(zip(self.time_ls, self.coupon_ls))

        self.time_to_mature = (self.maturity - self.today).days / 365
        self.YTM = None
        self.duration = None
        self.modified_duration = None
        self.convexity = None

    def value(self, y):
        p = 0
        df = 1 / (1 + y)
        for i in range(self.num_coupon):
            p += self.coupon_ls[i] * df ** (self.time_ls[i] / 365)
        return p

    def set_YTM(self, ytm):
        self.YTM = ytm

    def set_duration(self):
        if self.YTM is None:
            raise ValueError("YTM must be set before calculating duration.")
        d = 0
        for i in range(self.num_coupon):
            d += self.coupon_ls[i] * (self.time_ls[i] / 365) * (1 / (1 + self.YTM)**(1 + self.time_ls[i] / 365))
        d = d * ((1 + self.YTM) / self.ask_price)
        self.duration = d

    def set_modified_duration(self):
        if self.duration is None:
            raise ValueError("Duration must be set before calculating modified duration.")
        self.modified_duration = self.duration / (1 + self.YTM)

    def set_convexity(self):
        if self.YTM is None:
            raise ValueError("YTM must be set before calculating convexity.")
        c = 0
        for i in range(self.num_coupon):
            c += self.coupon_ls[i] * (self.time_ls[i] / 365) * ((self.time_ls[i] + 365) / 365) * (1 / (1 + self.YTM)**(2 + self.time_ls[i] / 365))
        c = c * (1 / (2 * self.ask_price))
        self.convexity = c

    def _calc_time_ls(self):
        next_coupon_date = self.next_coupon_date
        exact_date_ls = [next_coupon_date.strftime('%Y%m%d')]
        diff = (next_coupon_date - self.today).days
        time_ls = [diff]
        for _ in range(self.num_coupon - 1):
            next_coupon_date += DateOffset(months=6)
            exact_date_ls.append(next_coupon_date.strftime('%Y%m%d'))
            diff = (next_coupon_date - self.today).days
            time_ls.append(diff)
        return exact_date_ls, time_ls

    def _calc_coupon_ls(self):
        coupon_ls = [self.coupon] * self.num_coupon
        coupon_ls[-1] += self.face_value
        return coupon_ls
    

