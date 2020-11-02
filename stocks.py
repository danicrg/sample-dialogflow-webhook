import yfinance as yf
from datetime import datetime
from dateutil.parser import parse
import pandas as pd

def get_history(symbol='VHGEX', period='2mo'):
	equity = yf.Ticker(symbol)
	df = equity.history(period=period)[['Close']]
	df.reset_index(level=0, inplace=True)
	df.columns = ['ds', 'y']
	df = df.set_index('ds')

	return df

def compute_bb():
	df = get_history()

	# calculate Simple Moving Average with 20 days window
	sma = df.rolling(window=20).mean()
	exp = df.y.ewm(span=20, adjust=False).mean()

	# calculate the standar deviation
	rstd = df.rolling(window=20).std()

	upper_band = sma + 2 * rstd
	upper_band = upper_band.rename(columns={'y': 'upper'})
	lower_band = sma - 2 * rstd
	lower_band = lower_band.rename(columns={'y': 'lower'})

	# Making of plot
	bb = df.join(upper_band).join(lower_band).join(sma.rename(columns={'y': 'sma'})).join(rstd.rename(columns={'y': 'rstd'}))
	bb = bb.dropna()

	return bb

def plot_bb(bb):
	plt.style.use('dark_background')
	plt.figure(figsize=(10,10))
	plt.plot(bb['upper'], color='#ADCCFF', alpha=0.2, label='Bollinger Bands')
	plt.plot(bb['lower'], color='#ADCCFF', alpha=0.2)
	plt.plot(bb['y'], label='VHGEX')
	plt.plot(bb['sma'], linestyle='--', alpha=0.7, label='Simple Moving Average')
	plt.title('VHGEX Price and BB')
	plt.legend(loc='best')
	plt.fill_between(bb.index, bb['lower'], bb['upper'], color='#ADCCFF', alpha=0.2)

	ax = plt.gca()
	fig = plt.gcf()
	fig.autofmt_xdate()

	plt.ylabel('SMA and BB')
	plt.grid()
	plt.savefig('bollinger')


def get_price(parsed_date):
	df = get_history(period='10y')

	price = df['y'].loc[
		(df.index.day == parsed_date.day) &
		(df.index.month == parsed_date.month) &
		(df.index.year == parsed_date.year)]

	return price.values[0]

def get_recommendation(bb):
	today = bb['y'][-1]
	yesterday = bb['y'][-2]
	percentage_increase = 100 * (today - yesterday) / yesterday
	date = str(bb.index[-1]).split()[0]

	evolution = round((bb['y'][-1]-bb['sma'][-1])/(2*bb['rstd'][-1])*100)

	message = date + '\n'
	message += '{}% | {}$\n\n'.format(round(percentage_increase,2), round(today, 2))

	if evolution > 0:
	  message += '{}% recommended SELL for added rentability'.format(evolution)
	else:
  		message += '{}% recommended BUY for added rentability'.format(-evolution)

	return message



df = get_history()
bb = compute_bb()

date = '2020-10-05T12:00:00+01:00'
parsed_date = parse(date).replace(tzinfo=None)

print(parsed_date.strftime("%Y-%m-%d"), get_price(parsed_date))

print(get_recommendation(bb))









