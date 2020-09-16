import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error


def load_data(infile):
	df = pd.read_csv(infile,  usecols=('date_local', 'latitude', 'longitude', 'arithmetic_mean'))
	print(df.head())
	df.drop_duplicates(inplace=True, ignore_index=True)
	df = df.groupby(['date_local', 'latitude', 'longitude']).mean().reset_index()
	df['date_local'] = pd.to_datetime(df['date_local'])
	return df


infile = '.\\data\\PM2.5_20190101_20191231.csv'
o3 = load_data(infile)

# 37.687526 for O3 and PM2p5
# 35.0467 PM10

filtered = o3.loc[o3['latitude'] == 37.687526].reset_index()
series = filtered['arithmetic_mean']

# filtered['arithmetic_mean'].plot()
# plt.show()

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


X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions_wk = list()
predictions_dy = list()

for t in range(len(test)):
	model = ARIMA(history, order=(10,1,0))
	model_fit = model.fit()
	output = model_fit.forecast(7)
	yhat = output[6]
	predictions_wk.append(yhat)
	yhat = output[0]
	predictions_dy.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions_dy)
print('Test MSE: %.3f' % error)
# plot
plt.plot(test, label='observed')
plt.plot(predictions_dy, color='red', label='one day prediction')
plt.plot(range(6, len(X) - size + 6), predictions_wk, ls='--', color='red', label='one week prediction')
plt.legend()
plt.show()