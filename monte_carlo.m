returns_data = readtable('returns.csv');
DateReturns = returns_data.Date;
Returns_btc = returns_data.btc;
Returns_eth = returns_data.eth;
Returns_xrp = returns_data.xrp;
Y = [Returns_btc, Returns_eth, Returns_xrp];

% monte carlo model
Mdl = varm(3,4); %3 values
Mdl.SeriesNames = {'BTC','ETH','XRP'};
EstMdl = estimate(Mdl,Y);



% numobs = 1176; 
numobs = 100; 
testStart = find(year(DateReturns)==2018,1); % Where we start our forecast using Monte Carlo
SampleSize = length(Returns_btc);
TestWindow           = testStart : SampleSize;
FDates = dateshift(returns_data.Date(testStart),'end','day',1:numobs); % from 2018.1.1 to 2021.3.28 

rng(1); %For reproducibility

% numobs 
% Y(testStart-30:testStart,:) : Use last 2017.12.1 to 2018.1.1 as presample 
% 1000: run 1000 simulations for each time point
Ysim = simulate(EstMdl,numobs,'Y0',Y(testStart-364:testStart,:),'NumPaths',1000);

Ymean = mean(Ysim,3); % Calculate means
Ystd = std(Ysim,0,3); % Calculate std deviations

Zscore = norminv(0.2);
monte95 = abs(Ymean - Zscore(1).*Ystd); 

% use 2s.d. for 95 confidence interval when plotting the blue lines 
f = figure('visible', 'on');
subplot(3,1,1)
plot(returns_data.Date(1:end),Y(1:end,1),'k') % training data from 2017.1.1 to 2020.3.28
hold('on')
plot([returns_data.Date(testStart) FDates],[Y(testStart,1);Ymean(:,1)],'r') % mean in red line
plot([returns_data.Date(testStart) FDates],[Y(testStart,1);Ymean(:,1)]+2.*[0;Ystd(:,1)],'b') % 2sd above mean in blue line
plot([returns_data.Date(testStart) FDates],[Y(testStart,1);Ymean(:,1)]-2.*[0;Ystd(:,1)],'b') % 2sd above mean in blue line
title('BTC')
subplot(3,1,2)

plot(returns_data.Date(1:end),Y(1:end,2),'k')
hold('on')
plot([returns_data.Date(testStart) FDates],[Y(testStart,2);Ymean(:,2)],'r')
plot([returns_data.Date(testStart) FDates],[Y(testStart,2);Ymean(:,2)]+2.*[0;Ystd(:,2)],'b')
plot([returns_data.Date(testStart) FDates],[Y(testStart,2);Ymean(:,2)]-2.*[0;Ystd(:,2)],'b')
title('ETH')
subplot(3,1,3)
plot(returns_data.Date(1:end),Y(1:end,3),'k')
hold('on')
plot([returns_data.Date(testStart) FDates],[Y(testStart,3);Ymean(:,3)],'r')
plot([returns_data.Date(testStart) FDates],[Y(testStart,3);Ymean(:,3)]+2.*[0;Ystd(:,3)],'b')
plot([returns_data.Date(testStart) FDates],[Y(testStart,3);Ymean(:,3)]-2.*[0;Ystd(:,3)],'b')
title('XRP')
saveas(f,sprintf('./monte_carlo.fig'));

% vol for btc, eth, xrp
aggregate_df = [Returns_btc(TestWindow),monte95(:,1),Returns_eth(TestWindow),monte95(:,2),Returns_xrp(TestWindow),monte95(:,3)];
csvwrite('monte_carlo.csv',aggregate_df);