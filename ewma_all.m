returns_data = readtable('returns.csv');
DateReturns = returns_data.Date;
Returns_btc = returns_data.btc;
Returns_eth = returns_data.eth;
Returns_xrp = returns_data.xrp;

SampleSize = length(Returns_btc);
TestWindowStart      = find(year(DateReturns)==2018,1);
TestWindow           = TestWindowStart : SampleSize;

[ewma95_btc,ewma99_btc] = ewma(Returns_btc, DateReturns, 'BTC');
[ewma95_eth,ewma99_eth] = ewma(Returns_eth, DateReturns, 'ETH');
[ewma95_xrp,ewma99_xrp] = ewma(Returns_xrp, DateReturns, 'XRP');

% header:  [returns_btc, ewma95_btc, ewma99_btc, returns_eth, ewma95_etg, ewma99_eth, returns_xrp, ewma95_xrp, ewma99_xrp]
aggregate_df = [Returns_btc(TestWindow),ewma95_btc,ewma99_btc, Returns_eth(TestWindow),ewma95_eth,ewma99_eth,Returns_xrp(TestWindow),ewma95_xrp,ewma99_xrp];
csvwrite('ewma.csv',aggregate_df);