import pandas as pd
import numpy as np

return_dataset = pd.read_csv('processed_data/returns.csv')
np.random.seed(42)
# get the index from the df for 2018-01-01
i_2018 = return_dataset[return_dataset['Date']=='2018-01-01'].index[0]
return_all = return_dataset[['btc', 'eth', 'xrp']].to_numpy()
# total number of time points
T = len(return_dataset)

df_mc_95 = pd.DataFrame({"Date":[],
                         "btc":[],"var_95_btc":[],
                         "eth":[],"var_95_eth":[],
                         "xrp":[],"var_95_xrp":[]})

# Run Monte Carlo Simulations based on the predicted Volatility & assumed mean 0
# number of simulations
for n_sims in [1000,10000,100000]:
    for i in range (i_2018, T):
        # past 7 days data
        train_data = return_all[i - 7:i]
        # mean for respective crypto-currency
        mean_all = np.mean(train_data, axis=0)
        mean_btc = mean_all[0]
        mean_eth = mean_all[1]
        mean_xrp = mean_all[2]
        # std for respective crypto-currency
        std_all = np.std(train_data, axis=0)
        std_btc = std_all[0]
        std_eth = std_all[1]
        std_xrp = std_all[2]
        sim_returns_btc = np.random.normal(mean_btc, std_btc, n_sims)
        sim_returns_eth = np.random.normal(mean_eth, std_eth, n_sims)
        sim_returns_xrp = np.random.normal(mean_xrp, std_xrp, n_sims)
        v_var_95_btc = -np.percentile(sim_returns_btc, 5)
        v_var_95_eth = -np.percentile(sim_returns_eth, 5)
        v_var_95_xrp = -np.percentile(sim_returns_xrp, 5)
        returns_btc_eth_xrp = return_dataset.iloc[i,:]
        date = returns_btc_eth_xrp[0]
        v_return_btc = returns_btc_eth_xrp[1]
        v_return_eth = returns_btc_eth_xrp[2]
        v_return_xrp = returns_btc_eth_xrp[3]
        update_data = [date,v_return_btc,v_var_95_btc, v_return_eth,v_var_95_eth, v_return_xrp,v_var_95_xrp]
        df_mc_95.loc[i] = update_data
    df_mc_95.to_excel("results/mc_%d_95.xlsx"%n_sims,index=False)