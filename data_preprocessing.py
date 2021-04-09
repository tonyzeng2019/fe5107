import pandas as pd
import numpy as np
# data from 2017.1.2 to 2021.3.28
btc = pd.read_csv('data/BTC-USD.csv')
eth = pd.read_csv('data/ETH-USD.csv')
xrp = pd.read_csv('data/XRP-USD.csv')

# only using adj close data
btc_price = btc['Adj Close'].to_numpy()
eth_price = eth['Adj Close'].to_numpy()
xrp_price = xrp['Adj Close'].to_numpy()

date_array = btc['Date'].to_numpy()
price_dataset = pd.DataFrame({'Date': date_array, 'btc': btc_price, 'eth': eth_price, 'xrp': xrp_price})
# remove NA values price_dataset
price_dataset = price_dataset.dropna()

# convert price to returns and adjust length
# e.g. 1.1 $100, 1.2 : $120, return: 1.2 with ln(120) - ln(100)
# u(i) = ln(s(i)/s(i-1))
return_btc = np.diff(np.log(price_dataset.btc), n=1, axis=0)
return_eth = np.diff(np.log(price_dataset.eth), n=1, axis=0)
return_xrp = np.diff(np.log(price_dataset.xrp), n=1, axis=0)

return_dataset = pd.DataFrame({'Date': price_dataset.Date.to_numpy()[1:], 'btc': return_btc, 'eth': return_eth, 'xrp': return_xrp})
# export return
return_dataset.to_csv('processed_data/returns.csv', index=False)

# get the index from the df for 2018-01-01
i_2018 = return_dataset[return_dataset['Date']=='2018-01-01'].index[0]
return_dataset_2018 = return_dataset.iloc[i_2018:]
return_dataset_2018.to_csv('processed_data/returns_2018.csv', index=False)