from statsmodels.tsa.stattools import adfuller
import pandas as pd

return_dataset = pd.read_csv('processed_data/returns.csv')
def ads_test(values_cryptocurrency, str_crptocurrency):
    X = values_cryptocurrency
    result = adfuller(X)
    print("="*40)
    print("ADS Test for %s"%str_crptocurrency)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

ads_test(return_dataset.btc.values, "BTC")
ads_test(return_dataset.eth.values, "ETH")
ads_test(return_dataset.xrp.values, "XRP")