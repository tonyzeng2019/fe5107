# fe5107
1. Use data_preprocessing.py does data preprocessing (get log-return datasets for btc, eth and xrp) 
=> generate returns.csv & returns_2018.csv
2. Use ewma_single_currency.py to run EWMA on all 3 cryptocurrencies 
=> generate ewma_95.csv (respective returns & VAR at 95CI)
3. Use garch_single_currency.py to run garch one-one model
=> generate gammas.csv
4. Use monte_carlo_ewma to run Monte Carlo simulations with EWMA results 
=> generate ewma_mc_95.csv & ewma_mc_100000_95 (for 1000 simulations vs 100000 simulations)