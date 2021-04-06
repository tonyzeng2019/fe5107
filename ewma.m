function[EWMA95,EWMA99] = ewma(Returns, DateReturns, CryptoType)
    SampleSize = length(Returns);
    TestWindowStart      = find(year(DateReturns)==2018,1);
    TestWindow           = TestWindowStart : SampleSize;
    EstimationWindowSize = 2;

    pVaR = [0.05 0.01];

    Lambda = 0.94;
    Sigma2     = zeros(length(Returns),1);
    Sigma2(1)  = Returns(1)^2;

    for i = 2 : (TestWindowStart-1)
        Sigma2(i) = (1-Lambda) * Returns(i-1)^2 + Lambda * Sigma2(i-1);
    end

    Zscore = norminv(pVaR);
    EWMA95 = zeros(length(TestWindow),1);
    EWMA99 = zeros(length(TestWindow),1);

    for t = TestWindow
        k     = t - TestWindowStart + 1;
        Sigma2(t) = (1-Lambda) * Returns(t-1)^2 + Lambda * Sigma2(t-1);
        Sigma = sqrt(Sigma2(t));
        EWMA95(k) = -Zscore(1)*Sigma;
        EWMA99(k) = -Zscore(2)*Sigma;
    end

    f = figure('visible', 'on');
    plot(DateReturns(TestWindow),[EWMA95 EWMA99])
    ylabel('VaR')
    xlabel('Date')
    legend({'95% Confidence Level','99% Confidence Level'},'Location','Best')
    title(sprintf('VaR Estimation of %s Using the EWMA Method',CryptoType))
    saveas(f,sprintf('./%s.fig',CryptoType))
    
end
