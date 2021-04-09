import pandas as pd
import numpy as np
VAR_2018 = np.load('results/data_var.npy')
return_dataset_2018 = pd.read_csv('processed_data/returns_2018.csv')
np.random.seed(42)
df_mc_95 = pd.DataFrame({"btc":[],"var_95_btc":[],
                           "eth":[],"var_95_eth":[],
                           "xrp":[],"var_95_xrp":[]})
# Run Monte Carlo Simulations based on the predicted Volatility & assumed mean 0
for i in range (0,len(VAR_2018)):
    mean = 0
    std_all = np.sqrt(VAR_2018[i])
    std_btc = std_all[0]
    std_eth = std_all[1]
    std_xrp = std_all[2]
    n_sims = 100000 # number of simulations
    sim_returns_btc = np.random.normal(mean, std_btc, n_sims)
    sim_returns_eth = np.random.normal(mean, std_eth, n_sims)
    sim_returns_xrp = np.random.normal(mean, std_xrp, n_sims)
    v_var_95_btc = -np.percentile(sim_returns_btc, 5)
    v_var_95_eth = -np.percentile(sim_returns_eth, 5)
    v_var_95_xrp = -np.percentile(sim_returns_xrp, 5)
    returns_btc_eth_xrp = return_dataset_2018.iloc[i,:]
    v_return_btc = returns_btc_eth_xrp[1]
    v_return_eth = returns_btc_eth_xrp[2]
    v_return_xrp = returns_btc_eth_xrp[3]
    update_data = [v_return_btc,v_var_95_btc, v_return_eth,v_var_95_eth, v_return_xrp,v_var_95_xrp]
    df_mc_95.loc[i] = update_data
df_mc_95.to_excel("results/ewma_mc_100000_95.xlsx",index=False)