import numpy as np
import scipy
import pandas as pd
from arch import arch_model
from scipy.stats import norm

class garchOneOne(object):

    def __init__(self, logReturns):
        # upscale by 100 for better garch model performance
        self.logReturns = logReturns * 100
        self.sigma_2 = self.garch_filter(self.garch_optimization())
        self.coefficients = self.garch_optimization()

    def garch_filter(self, parameters):
        "Returns the variance expression of a GARCH(1,1) process."

        # Slicing the parameters list
        omega = parameters[0]
        alpha = parameters[1]
        beta = parameters[2]

        # Length of logReturns
        length = len(self.logReturns)

        # Initializing an empty array
        sigma_2 = np.zeros(length)

        # Filling the array, if i == 0 then uses the long term variance.
        for i in range(length):
            if i == 0:
                sigma_2[i] = omega / (1 - alpha - beta)
            else:
                sigma_2[i] = omega + alpha * self.logReturns[i - 1] ** 2 + beta * sigma_2[i - 1]

        return sigma_2

    # Defines the log likelihood sum to be optimized given the parameters
    def garch_loglikehihood(self, parameters):
        length = len(self.logReturns)

        sigma_2 = self.garch_filter(parameters)

        loglikelihood = - np.sum(-np.log(sigma_2) - self.logReturns ** 2 / sigma_2)
        return loglikelihood

    # Optimizes the log likelihood function and returns estimated coefficients
    def garch_optimization(self):
        # Parameters initialization
        parameters = [.1, .05, .92]

        # Parameters optimization, scipy does not have a maximize function, so we minimize the opposite of the equation described earlier
        opt = scipy.optimize.minimize(self.garch_loglikehihood, parameters,
                                      bounds=((.001, 1), (.001, 1), (.001, 1)))

        variance = .01 ** 2 * opt.x[0] / (1 - opt.x[1] - opt.x[2])  # Times .01**2 because it concerns squared returns

        return np.append(opt.x, variance)

# data: return data
# cryptoType: "BTC"/"ETH","XRP
# conf_interval
# dist_type: distribution type for garch model (default: normal)
# return sigma from garch
def run_garch(data, cryptoType, conf_interval, dist_type='normal'):
    print("=" * 40)
    print("=" * 40)
    print("Running Garch 1,1 model for %s" % cryptoType)
    model = garchOneOne(data)
    # upscale by 100 for better model performance, as garch model works better when y between 1 - 1000
    arch_m = arch_model(data * 100, mean='Zero', vol='GARCH', dist=dist_type, rescale=False)
    arch_m = arch_m.fit()
    # downscale by 100 back to original value
    return np.sqrt(model.sigma_2) / 100

return_dataset = pd.read_csv('processed_data/returns.csv')
return_dataset_2018 = pd.read_csv('processed_data/returns_2018.csv')
# get the index from the df for 2018-01-01
i_2018 = return_dataset[return_dataset['Date']=='2018-01-01'].index[0]
# Get 95% confidence interval
pVar = 0.05
Zscore = norm.ppf(pVar)
btc_sigma = run_garch(return_dataset.btc.to_numpy(), "BTC", pVar)
eth_sigma = run_garch(return_dataset.eth.to_numpy(), "ETH", pVar)
xrp_sigma = run_garch(return_dataset.xrp.to_numpy(), "XRP", pVar)

var_btc = np.abs(-norm.ppf(0.05)*btc_sigma[363:])
var_eth = np.abs(-norm.ppf(0.05)*eth_sigma[363:])
var_xrp = np.abs(-norm.ppf(0.05)*xrp_sigma[363:])

pVar = 0.05

df_garch_95 = pd.DataFrame({'btc': return_dataset_2018.btc, 'var_95_btc': var_btc,
              'eth': return_dataset_2018.eth, 'var_95_eth': var_eth,
              'xrp': return_dataset_2018.xrp, 'var_95_xrp': var_xrp})
df_garch_95.to_excel('results/garch_95.xlsx', index=False)
