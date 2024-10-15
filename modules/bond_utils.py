from Bond.QuoteBond import Bond
from Bond.PortfolioBond import PortBond
import pandas as pd
import numpy as np

def combine_portfolio(bond_list):
    """
    Combines a list of bonds into a single portfolio, calculating the total price and cumulative coupon payments.

    Parameters:
    bond_list (list): List of Bond objects to combine.

    Returns:
    PortBond: A portfolio object containing aggregated coupon payments, time periods, and total price.
    """
    portfolio = PortBond()
    total_price = 0
    coupon_frames = []

    for bond in bond_list:
        bond: Bond
        total_price += bond.ask_price
        coupon_frames.append(pd.DataFrame.from_dict(bond.coupon_dic, orient='index', columns=[f"{bond.identifier}"]))

    portfolio.set_price(total_price)
    full_df = pd.concat(coupon_frames, axis=1)
    total_coupon_payment = full_df.sum(axis=1)
    
    portfolio.set_coupon_ls(total_coupon_payment.tolist())
    portfolio.set_time_ls(total_coupon_payment.index.tolist())
    portfolio.set_num_coupon(len(total_coupon_payment))

    return portfolio

def categorize_by_maturity(row):
    """
    Categorizes bonds based on remaining years to maturity into portfolios A, B, C, or D.

    Parameters:
    row (pd.Series): A row of the DataFrame containing bond information.

    Returns:
    str or np.nan: Portfolio category based on maturity or NaN if no category matches.
    """
    if 2 <= row['remain year'] <= 7:
        return 'D'
    elif 7 < row['remain year'] <= 10:
        return 'C'
    elif 10 < row['remain year'] <= 15:
        return 'B'
    elif row['remain year'] > 15:
        return 'A'
    return np.nan