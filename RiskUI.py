import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import norm
import matplotlib.mlab as mlab
import math

app = dash.Dash(__name__)

app.layout = html.Div(children = [
	html.H1('Portfolio VAR Calculator',style = {'text-align':'center','font-family':'Arial','margin-top':'50px'}),
	
	html.Div(children = [
		
		html.Div(children = [
			
			html.Div(children = [
				html.H4('Please Input Bitcoin (BTC) Value:',style = {'margin-left':'25px','font-family':'Arial','display':'inline-block'}),
				html.Div(id='BTC_value', style={'margin-left':'25px','font-family':'Arial','display':'inline-block'})			]
			),
			html.Br(),
			dcc.RangeSlider(
				id='BTC slide',
				min=0,
				max=10000,
				step=1,
				value=[0],
				updatemode = 'drag',
				marks = {
					5000: {'label':'5000','style' : {'font-family':'Arial'}},
					10000: {'label':'10000','style' : {'font-family':'Arial'}},
					0: {'label':'0','style' : {'font-family':'Arial'}},
				}
			),
			
			html.Br(),
			html.Br(),
			html.Div(children = [
				html.H4('Please Input Ethereum (ETH) Value:',style = {'margin-left':'25px','font-family':'Arial','display':'inline-block'}),
				html.Div(id='ETH_value', style={'margin-left':'25px','font-family':'Arial','display':'inline-block'})			]
			),
			html.Br(),
			dcc.RangeSlider(
				id='ETH slide',
				min=0,
				max=10000,
				step=1,
				value=[0],
				updatemode = 'drag',
				marks = {
					5000: {'label':'5000','style' : {'font-family':'Arial'}},
					10000: {'label':'10000','style' : {'font-family':'Arial'}},
					0: {'label':'0','style' : {'font-family':'Arial'}},
				}
			),
			
			html.Br(),
			html.Br(),
			html.Div(children = [
				html.H4('Please Input Ripple (XRP) Value:',style = {'margin-left':'25px','font-family':'Arial','display':'inline-block'}),
				html.Div(id='XRP_value', style={'margin-left':'25px','font-family':'Arial','display':'inline-block'})			]
			),
			html.Br(),
			dcc.RangeSlider(
				id='XRP slide',
				min=0,
				max=10000,
				step=1,
				value=[0],
				updatemode = 'drag',
				marks = {
					5000: {'label':'5000','style' : {'font-family':'Arial'}},
					10000: {'label':'10000','style' : {'font-family':'Arial'}},
					0: {'label':'0','style' : {'font-family':'Arial'}},
				}
			),
			
			html.Br(),
			html.Br(),
			html.Br(),
			html.Br(),
			html.Div(children = [
				html.H4('Portofolio Insights:',
					style = {'margin-left':'25px','font-family':'Arial'}),
				html.Div(children = [
					html.H4('Your 95% Portfolio 1-Day Value at Risk in Dollar:',style = {'margin-left':'25px','font-family':'Arial','display':'inline-block'}),
					html.Div(id='dollar_var', style={'margin-left':'25px','font-family':'Arial','display':'inline-block','color':'red'})			]
				),
				html.Div(children = [
					
					html.H4('Your 95% Portfolio 1-Day Value at Risk in Percentage:',style = {'margin-left':'25px','font-family':'Arial','display':'inline-block'}),
					html.Div(id='percentage_var', style={'margin-left':'25px','font-family':'Arial','display':'inline-block','color':'red'})			]
				)
			])
	],style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw','width':'600px'}),

	html.Div(children = [
		html.H4('Portfolio Weight Distribution Graph:',style = {'text-align':'center','font-family':'Arial'}),
		dcc.Graph(id = 'weight_pie')
	], style={'display': 'inline-block', 'vertical-align': 'top','width':'500px','margin-left':'200px'})])])

@app.callback(
	Output('BTC_value','children'),
	Output('ETH_value','children'),
	Output('XRP_value','children'),
	Output('dollar_var','children'),
	Output('percentage_var','children'),
	Output("weight_pie", "figure"),
	Input('BTC slide','value'),
	Input('ETH slide','value'),
	Input('XRP slide','value'))

def return_input(BTC,ETH,XRP):
	BTC_value = '$ '+ str(BTC[0])
	ETH_value = '$ '+ str(ETH[0])
	XRP_value = '$ '+ str(XRP[0])
	total_amount = int(BTC[0]) + int(ETH[0]) + int(XRP[0])
	if total_amount ==0:
		total_amount = 0.0001
	w_btc = float(int(BTC[0]) / total_amount)
	w_eth = float(int(ETH[0]) / total_amount)
	w_xrp = float(int(XRP[0]) / total_amount)
	
	VAR = np.load('data_var.npy')
	COV = np.load('data_cov.npy')
	
	pVar = 0.05
	Zscore = norm.ppf(pVar)
	weights = np.array([w_btc,w_eth,w_xrp]) # assume equal weightage
	T = len(VAR)
	portfolioVariance = np.zeros(T)
	
	def portfolio_daily_var(w1,w2,w3,v1,v2,v3,cov12,cov13,cov23):
		return (w1**2)*v1 + (w2**2)*v2 + (w3**2)*v3 \
			+ 2*w1*w2*cov12 + 2*w1*w3*cov13 + 2*w2*w3*cov23
		
	for i in range(0,T):
		portfolioVariance[i] = portfolio_daily_var(w_btc,w_eth,w_xrp,
									VAR[i,0],VAR[i,1],VAR[i,2],
									COV[i,0],COV[i,1],COV[i,2])
	EWMA95 = np.zeros(T)
	EWMA95[0] = portfolioVariance[0]
		
	for t in range(1,T):
		Sigma = math.sqrt(portfolioVariance[t])
		EWMA95[t] = -Zscore*Sigma
	
	percentage = EWMA95[-1]
	dollar = total_amount* EWMA95[-1]
	
	dollar_var = '$ '+ str(round(dollar,2))
	percentage_var = str(round((percentage*100),2)) + ' %'
	
	df = pd.DataFrame({'coins': ['BTC', 'ETH', 'XRP'],
		'weight': [w_btc,w_eth,w_xrp]})
	
	fig = px.pie(df, values='weight', names='coins', color_discrete_sequence=px.colors.sequential.RdBu)
	
	return BTC_value,ETH_value,XRP_value,dollar_var,percentage_var,fig

app.run_server(debug=True)
