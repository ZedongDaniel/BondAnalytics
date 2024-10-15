import numpy as np

def equal_value_position(series, allocation=100000000, note_par=1000):
    """
    Calculates position sizes to achieve equal value allocation for each bond in the series.

    Parameters:
    series (pd.Series): Series of bond prices.
    allocation (float): Total allocation amount.
    note_par (float): Par value of each bond.

    Returns:
    np.ndarray: Array of position sizes for each bond.
    """
    num_bonds = len(series)
    positions = (1 / num_bonds) * (allocation / series) / note_par
    return positions

def calculate_portfolio_statistics(df, allocation=100000000):
    """
    Calculates value-weighted portfolio statistics including YTM, duration, modified duration, and convexity.

    Parameters:
    df (pd.DataFrame): DataFrame containing bond data and position information.
    allocation (float): Total allocation amount.

    Returns:
    tuple: Weighted YTM, duration, modified duration, and convexity.
    """
    weights = (df['Ask Price'] * df['position'] * 1000) / allocation

    weighted_ytm = weights @ df['ytm']
    weighted_duration = weights @ df['duration']
    weighted_modified_duration = weights @ df['md']
    weighted_convexity = weights @ df['c']

    return weighted_ytm, weighted_duration, weighted_modified_duration, weighted_convexity

def equal_duration_position_v1(df, allocation=100000000, note_par=1000):
    """
    Calculates position sizes for an equal-duration portfolio using portfolio duration for each bond.

    Parameters:
    df (pd.DataFrame): DataFrame with bond durations and ask prices.
    allocation (float): Total allocation amount.
    note_par (float): Par value of each bond.

    Returns:
    np.ndarray: Array of position sizes based on duration weighting.
    """
    inverse_duration_sum = (1 / df['duration']).sum()
    positions = allocation / (df['Ask Price'] * df['duration'] * inverse_duration_sum) / note_par
    return positions

def equal_duration_position_v2(df, allocation=400000000):
    """
    Alternative calculation for position sizes in an equal-duration portfolio using bond values and durations.

    Parameters:
    df (pd.DataFrame): DataFrame containing bond data.
    allocation (float): Total allocation amount.

    Returns:
    np.ndarray: Array of position sizes based on duration weighting and bond values.
    """
    inverse_duration_sum = (1 / df['d']).sum()
    positions = allocation / (df['Val'] * df['d'] * inverse_duration_sum)
    return positions