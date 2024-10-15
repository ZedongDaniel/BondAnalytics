from Bond.QuoteBond import Bond
from Bond.PortfolioBond import PortBond
from modules.NonlinearSolver import NonlinaerSolver
from modules.bond_utils import combine_portfolio, categorize_by_maturity
from modules.portfolio_utils import equal_value_position, calculate_portfolio_statistics, equal_duration_position_v1, equal_duration_position_v2
from modules.visualization import plot_pnl_surface
import pandas as pd
import numpy as np

if __name__ == "__main__":
    bond_ls = []
    with open(f"Data/us_treasury_data_20230905.csv", "r") as file:
        data = file.readlines()[1:]
        for line in data:
            bond_ls.append(Bond(line))

    solver = NonlinaerSolver(lend= 0.0, rend = 1.0,acc= 1e-6)
    for bond in bond_ls:
        bond: Bond
        bond.set_YTM(solver.bisection(bond))
        bond.set_duration()
        bond.set_modified_duration()
        bond.set_convexity()

    port_A , port_B, port_C, port_D= [], [], [], []
    for bond in bond_ls:
        bond: Bond
        if 2 <= bond.time_to_mature <= 7:
            port_D.append(bond)
        elif 7 < bond.time_to_mature <= 10:
            port_C.append(bond)
        elif 10 < bond.time_to_mature <= 15:
            port_B.append(bond)
        elif bond.time_to_mature > 15:
            port_A.append(bond)

    
    port_ls = [combine_portfolio(port_A),combine_portfolio(port_B),combine_portfolio(port_C),combine_portfolio(port_D)]

    solver = NonlinaerSolver(lend= 0.0, rend = 1.0,acc= 1e-6)
    for port in port_ls:
        port: PortBond
        port.set_YTM(solver.bisection(port))
        port.set_duration()
        port.set_modified_duration()
        port.set_convexity()
    
    port_table = pd.DataFrame(columns=['A', 'B', 'C', 'D'])
    for i, port in enumerate(port_ls):
        s = pd.Series({
            'ytm': port.YTM,
            'd': port.duration,
            'md': port.modified_duration,
            'c': port.convexity
        })
        port_table.iloc[:, i] = round(s, 5)
    print("Compute equal value portfolio (YTM, Duration,Convexity) by aggregating cashflow")
    print(port_table.T)

    df = pd.read_csv("Data/us_treasury_data_20230905.csv").iloc[:,:14]
    time_ls = []
    ytm_ls = []
    duration_ls = []
    md_ls = []
    c_ls = []
    for bond in bond_ls:
        bond: Bond
        time_ls.append(bond.time_to_mature)
        ytm_ls.append(bond.YTM)
        duration_ls.append(bond.duration)
        md_ls.append(bond.modified_duration)
        c_ls.append(bond.convexity)

    df['remain year'] = time_ls
    df['ytm'] = ytm_ls
    df['duration'] = duration_ls
    df['md'] = md_ls
    df['c'] = c_ls

    df['portfolio'] = df.apply(categorize_by_maturity, axis=1)
    df_port_equal_val = df.dropna(subset=['portfolio']).copy()
    df_port_equal_val['position'] = df_port_equal_val.groupby('portfolio',group_keys = False)["Ask Price"].apply(lambda x: equal_value_position(x))
    stats_table = df_port_equal_val.groupby('portfolio',group_keys = False).apply(lambda x: calculate_portfolio_statistics(x), include_groups=False)
    stats_table = pd.DataFrame(stats_table.tolist(), index=stats_table.index, columns=['ytm', 'd', 'md', 'c'])
    print("\nCompute equal value portfolio (YTM, Duration,Convexity) by value weighted sum of the portfolio component")
    print(round(stats_table, 5))


    b = np.array([[15.30898,  3.85018],
                  [144.61398, 9.57503]
                  ])
    y = np.array([[-7.55590],
                  [-31.92781]])
    x = np.linalg.solve(b, y)
    pos_c = 1 * 1e9 / 1000
    pos_a = x[0][0] * 1e9 / 1000
    pos_d = x[1][0] * 1e9 / 1000
    print(f"\nNumber of unit trade in portfolio C: {pos_c:.3f} in units of $1,000-par bonds")
    print(f"Number of unit trade in portfolio A: {pos_a:.3f} in units of $1,000-par bonds")
    print(f"Number of unit trade in portfolio D: {pos_d:.3f} in units of $1,000-par bonds")
    print(f"total value: {(pos_c + pos_a + pos_d) * 1000:.3f} dollars")

    print("\nbutterfly trading:")
    yield_change_a, yield_change_c, yield_change_d= -100 / 1e4, -50 / 1e4, -80 / 1e4
    port_a_change = (-15.30898 * (yield_change_a) + 144.61398 * (yield_change_a)**2) * pos_a * 1000
    port_c_change = (-7.55590 * (yield_change_c) + 31.92781 * (yield_change_c)**2) * pos_c * 1000
    port_d_change = (-3.85018 * (yield_change_d) + 9.57503 * (yield_change_d)**2) * pos_d * 1000
    total_change = port_a_change + port_c_change + port_d_change
    print(f"When A go down {100}bp; C go down {50}bp; D go down {80}bp, total PnL: {total_change:.3f}")

    yield_change_a, yield_change_c, yield_change_d= 100 / 1e4, 150 / 1e4, 80 / 1e4
    port_a_change = (-15.30898 * (yield_change_a) + 144.61398 * (yield_change_a)**2) * pos_a * 1000
    port_c_change = (-7.55590 * (yield_change_c) + 31.92781 * (yield_change_c)**2) * pos_c * 1000
    port_d_change = (-3.85018 * (yield_change_d) + 9.57503 * (yield_change_d)**2) * pos_d * 1000
    total_change = port_a_change + port_c_change + port_d_change
    print(f"When A go up {100}bp; C go up {150}bp; D go up {80}bp, total PnL: {total_change:.3f}")

    plot_pnl_surface(pos_a, pos_c, pos_d)
    
    df_port_equal_duration = df.dropna(subset=['portfolio']).copy()
    df_port_equal_duration['position'] = df_port_equal_duration.groupby('portfolio', group_keys=False).apply(lambda x: equal_duration_position_v1(x), include_groups=False)
    stats_table_2 = df_port_equal_duration.groupby('portfolio',group_keys = False).apply(lambda x: calculate_portfolio_statistics(x), include_groups=False)
    stats_table_2 = pd.DataFrame(stats_table_2.tolist(), index=stats_table_2.index, columns=['ytm', 'd', 'md', 'c'])

    stats_table_2['Val'] = [100000000] * 4
    stats_table_2['pos'] = equal_duration_position_v2(stats_table_2)
    print("\nCompute equal duration portfolio (YTM, Duration,Convexity) by value weighted sum of the portfolio component")
    print(stats_table_2)

    




    









    



    



            





    


        


    