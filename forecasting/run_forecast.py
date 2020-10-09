import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error
import numpy as np
import os

def load_data(infile, VARIABLES):

# 	cols = ['Date', 'Lat', 'Lon'] + VARIABLES
	cols = ['Date', 'Lat', 'Zipcode'] + VARIABLES
	df = pd.read_csv(infile,  usecols=cols)
# 	return df.reset_index()
	return df


VARIABLES = ['O3', 'PM10', 'NO2']
infile = os.path.join(
			os.path.dirname(os.getcwd()), # <- this is the parent dir
			'processed_data',
			'aqs_california_merged_zipcode_20160101_20200831.csv')
df = load_data(infile, VARIABLES)

print(df.head(10))

# Remove whitespace from zipcode column
df['Zipcode'] = df['Zipcode'].str.strip()

# filtered = df.loc[df['Lat'] == 33.996360].reset_index()
filtered = df.loc[df['Zipcode'] == '93062']
filtered.head()

import sys
sys.path.insert(1, os.getcwd() + '../forecasting')
import forecast_20201008


series = filtered[VARIABLES].fillna(method='bfill').dropna()
print(series.head())
print(series.tail())

### import forecast module and do multivariate time analysis
f = forecast_20201008.Forecast(series)
f.get_model()
f.get_lag()

# Run Forecast
f.train_model()

# Save model
f.save_model(savefile = 'arima_O3_PM10_NO2_zipcode-93062.sav')

# Forecast
f.run_forecast()
f.plot_prediction(savefile = '../figures/o3-pm2p5-forecast-test.png')



#################### IGNORE THINGS BELOW THIS COMMENT FOR NOW - CONTAINS OLD CODE I WANT TO KEEP


# autocorrelation_plot(filtered['arithmetic_mean'])
# plt.show()
### Evidence of positive correlation. perhaps significant up to X days
### X = 30 for O3
### X = 10 for PM2.5
### X = 10 for PM10


# model = ARIMA(filtered['arithmetic_mean'], order=(10,1,0))
# model_fit = model.fit()
# print(model_fit.summary())
# # plot residual errors
# residuals = pd.DataFrame(model_fit.resid)
# residuals.plot()
# plt.show()
# residuals.plot(kind='kde')
# plt.show()
# print(residuals.describe())


### Univariate ARIMA model

# X = series.values
# size = int(len(X) * 0.66)
# train, test = X[0:size], X[size:len(X)]
# history = [x for x in train]
# predictions_wk = list()
# predictions_dy = list()

# for t in range(len(test)):
# 	model = ARIMA(history, order=(30,1,0))
# 	model_fit = model.fit()
# 	output = model_fit.forecast(7)
# 	yhat = output[6]
# 	predictions_wk.append(yhat)
# 	yhat = output[0]
# 	predictions_dy.append(yhat)
# 	obs = test[t]
# 	history.append(obs)
# 	print('predicted=%f, expected=%f' % (yhat, obs))
# error = mean_squared_error(test, predictions_dy)
# print('Test MSE: %.3f' % error)
# # plot
# plt.plot(test, label='observed')
# plt.plot(predictions_dy, color='red', label='one day prediction')
# #plt.plot(range(6, len(X) - size + 6), predictions_wk, ls='--', color='red', label='one week prediction')
# plt.legend()
# plt.xlabel('Day')
# plt.ylabel('Concentration [ppb]')
# plt.show()

### Multivariate VAR model


#model = VAR(series)

#results = model.fit(maxlags=90, ic='aic')

# aic = []
# for i in range(90):
# 	result = model.fit(i)
# 	aic.append(result.aic)

# #plt.plot(range(90),  aic); plt.show()

# results = model.fit(7)
# print(results.summary())
# #results.plot_acorr()
# results.plot_forecast(10)
# plt.show()

# X = series.values
# size = int(len(X) * 0.8)
# train, test = X[0:size], X[size:len(X)]
# history = [x for x in train]
# predictions_wk = list()
# predictions_dy = list()
# for t in range(len(test)):
# 	model = VAR(history)
# 	model_fit = model.fit(10, ic='aic')
# 	output = model_fit.forecast(history[-10:], 10)
# 	yhat = output[6][1]
# 	predictions_wk.append(yhat)
# 	yhat = output[0]
# 	predictions_dy.append(yhat)
# 	obs = test[t]
# 	history.append(obs)
# 	#print('predicted=%f, expected=%f' % (yhat, obs))
# #error = mean_squared_error(test, predictions_dy)
# #print(error)
# # plot
# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,6))
# ax1.plot(test[:,0], label='observed')
# ax1.plot([i[0] for i in predictions_dy], color='red', label='one day prediction')
# ax2.plot(test[:,1], label='observed')
# ax2.plot([i[1] for i in predictions_dy], color='red', label='one day prediction')


# #plt.plot(range(6, len(X) - size + 6), predictions_wk, ls='--', color='red', label='one week prediction')


# plt.legend()
# ax1.set_xlabel('Day')
# ax1.set_ylabel('Concentration [ppb]')
# ax2.set_xlabel('Day')
# ax2.set_ylabel('Temperature [C]')

# plt.show()
