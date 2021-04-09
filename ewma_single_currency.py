import pandas as pd
import numpy as np
from scipy.stats import norm
from numpy import asarray
from numpy import save
# data from 2017.1.1 to 2021.3.28
return_dataset = pd.read_csv('processed_data/returns.csv')
return_dataset_2018 = pd.read_csv('processed_data/returns_2018.csv')
# get the index from the df for 2018-01-01
i_2018 = return_dataset[return_dataset['Date']=='2018-01-01'].index[0]
return_all = return_dataset[['btc', 'eth', 'xrp']].to_numpy()
# total number of time points
T = len(return_dataset)
VAR = np.full([T,3], np.nan)
COV = np.full([T,3], np.nan)
lmbda = 0.94
# get the covariance of the data
S = np.cov(return_all, rowvar = False)
# store the S matrix (T * covariance matrix)
S_matrix = np.full([T,3,3], np.nan)
S_matrix[0,] = S
VAR[0,] = [S[0,0],S[1,1],S[2,2]]
COV[0,] = [S[0,1],S[0,2],S[1,2]]

for i in range(1,T):
    S = lmbda * S_matrix[i-1] + (1-lmbda) * np.transpose(np.asmatrix(return_all[i - 1])) * np.asmatrix(return_all[i - 1])
    S_matrix[i] = S
    VAR[i,] = [S[0,0],S[1,1],S[2,2]] # Var_btc, Var_eth, Var_xrp
    COV[i,] = [S[0,1],S[0,2],S[1,2]] # Cov_btc_eth, Cov_btc_xrp, Cov_eth_xrp

# number of time points since 2018
T_2018 = T - i_2018
VAR_2018 = np.full([T_2018,3], np.nan)
COV_2018 = np.full([T_2018,3], np.nan)

# Get 95% confidence interval
pVar = 0.05
Zscore = norm.ppf(pVar)
# Get individual EWMA95
df_ewma_95 = pd.DataFrame({"btc":[],"var_95_btc":[],
                           "eth":[],"var_95_eth":[],
                           "xrp":[],"var_95_xrp":[]})

count = 0
for i in range(i_2018,T):
    VAR_2018[count,] = VAR[i,:]
    COV_2018[count,] = COV[i,:]
    # value at risk var value at 95% CI
    v_var_95_btc, v_var_95_eth, v_var_95_xrp = - Zscore * np.sqrt(VAR[i,:])
    # corresponding btc eth xrp returns
    returns_btc_eth_xrp = return_dataset.iloc[i,:]
    v_return_btc = returns_btc_eth_xrp[1]
    v_return_eth = returns_btc_eth_xrp[2]
    v_return_xrp = returns_btc_eth_xrp[3]
    update_data = [v_return_btc,v_var_95_btc, v_return_eth,v_var_95_eth, v_return_xrp,v_var_95_xrp]
    df_ewma_95.loc[count] = update_data
    count += 1

df_ewma_95.to_excel("results/ewma_95.xlsx",index=False)
# Save numpy array as npy file (used for later-on VAR for actual portfolio
data_var_2018 = asarray(VAR_2018)
# save to npy file
save('results/data_var.npy', data_var_2018)
data_cov_2018 = asarray(COV_2018)
# save to npy file
save('results/data_cov.npy', data_cov_2018)