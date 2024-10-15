from Bond.BaseBond import BondAbstract


class PortBond(BondAbstract):
    def __init__(self) -> None:
        self.ask_price = 0.0
        self.coupon_ls = []
        self.exact_date_ls = []
        self.time_ls = []
        self.YTM = None
        self.num_coupon = 0
        self.duration = None
        self.modified_duration = None
        self.convexity = None

    def set_YTM(self, ytm):
        self.YTM = ytm

    def set_price(self, price):
        self.ask_price = price

    def set_time_ls(self, time_ls):
        self.time_ls = time_ls
    
    def set_coupon_ls(self, coupon_ls):
        self.coupon_ls = coupon_ls

    def set_num_coupon(self, num):
        self.num_coupon = num

    def value(self, y):
        if not self.coupon_ls or not self.time_ls:
            raise ValueError("Coupon list and time list must be set before calculating value.")
        p = 0
        df = 1 / (1 + y)
        for i in range(self.num_coupon):
            p += self.coupon_ls[i] * df ** (self.time_ls[i] / 365)
        return p
    
    def set_duration(self):
        if self.YTM is None:
            raise ValueError("YTM must be set before calculating duration.")
        if not self.coupon_ls or not self.time_ls:
            raise ValueError("Coupon list and time list must be set before calculating duration.")
        d = 0
        for i in range(self.num_coupon):
            d += self.coupon_ls[i] * (self.time_ls[i] / 365) * (1 / (1 + self.YTM)**(1 + self.time_ls[i] / 365))
        d = d * ((1 + self.YTM) / self.ask_price)
        self.duration = d

    def set_modified_duration(self):
        if self.duration is None:
            raise ValueError("Duration must be calculated before calculating modified duration.")
        self.modified_duration = self.duration / (1 + self.YTM)

    def set_convexity(self):
        if self.YTM is None:
            raise ValueError("YTM must be set before calculating convexity.")
        if not self.coupon_ls or not self.time_ls:
            raise ValueError("Coupon list and time list must be set before calculating convexity.")
        c = 0
        for i in range(self.num_coupon):
            c += self.coupon_ls[i] * (self.time_ls[i] / 365) * ((self.time_ls[i] + 365) / 365) * (1 / (1 + self.YTM)**(2 + self.time_ls[i] / 365))
        c = c * (1 / (2 * self.ask_price))
        self.convexity = c
    

