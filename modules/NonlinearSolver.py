from Bond.BaseBond import BondAbstract


class NonlinaerSolver:
    def __init__(self, lend, rend, acc) -> None:
        self.target = 0.0
        self.lend = lend
        self.rend = rend
        self.acc = acc
        self.iter_num = 0

    def bisection(self, bond:BondAbstract):
        self.iter_num = 0
        self.target = bond.ask_price
        left = self.lend
        right = self.rend
        mid = (left + right) / 2

        y_left = bond.value(left) - self.target
        y_mid = bond.value(mid) - self.target

        while (mid - left) > self.acc:
            self.iter_num += 1
            if (y_left > 0 and y_mid > 0) or (y_left < 0 and y_mid < 0):
                left = mid
                y_left = y_mid

            else:
                right = mid

            mid = (left + right) / 2
            y_mid = bond.value(mid) - self.target
            
        
        return mid
    


    







    

    

    
