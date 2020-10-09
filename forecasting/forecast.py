import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Forecast():

	def __init__(self, df):

		self.df = df
		self.df_diff = df.diff().dropna()

	def get_model(self):
		'''
		Determines which type of model to use
		If only one column of time-series data, then run univariate model (ARIMA)
		Else, run multivariate model (VAR)
		'''

		if self.df.shape[1] == 1:
			from statsmodels.tsa.arima.model import ARIMA
			self.model = ARIMA(self.df_diff)

		else:
			from statsmodels.tsa.api import VAR
			self.model = VAR(self.df_diff)

	def get_lag(self, nlag=50, ic='aic', plotting=True):
		'''
		Returns the lag order minimizing the give information criterion
		INPUTS: nlag, int: max number of lags to loop through
				ic, str: information criterion to measure
				plotting, bool: optionally plot results
		'''

		result = []
		for i in range(nlag):
			result.append( getattr(self.model.fit(i), ic) )

		min_ic = min(result)
		min_lag = [i for i, j in enumerate(result) if j == min_ic][0]

		self.ic = ic
		self.lag = min_lag

		if plotting:

			plt.plot(result)
			plt.xlabel('lag [days]', fontsize=14)
			plt.ylabel(ic, fontsize=14)
			plt.show()

	def train_model(self):
		self.X = self.df_diff.values
		self.model_fit = self.model.fit(self.lag, self.ic)

	def save_model(self, savefile = 'saved_model.sav'):
		import pickle
		pickle.dump(self.model_fit, open(savefile, 'wb'))

	def run_forecast(self, nobs=7):
		self.predictions = self.model_fit.forecast(self.X[-self.lag:], nobs)

	def plot_prediction(self, savefile=None):
		nrow, ncol = self.df.shape

		fig, axes = plt.subplots(nrows=ncol, ncols=1, figsize=(10, 3 * self.df.shape[1]))
		for i, ax in enumerate(axes):
			ax.plot(self.predictions[:,i], label='observed')
			ax.set_xlabel('forecast [days]')
			ax.set_ylabel(self.df.columns[i] + ' daily difference')
		plt.show()

		fig, axes = plt.subplots(nrows=ncol, ncols=1, figsize=(10, 3 * self.df.shape[1]))
		ndays = range(nrow + len(self.predictions))
		for i, ax in enumerate(axes):
			ax.plot(ndays[:nrow], self.df.values[:,i], color='k', label='observed')
			print([self.df.values[-1,i]], self.predictions[:,i])
			print([self.df.values[-1,i]] + list(self.predictions[:,i]))
			print(np.cumsum([self.df.values[-1,i]] + list(self.predictions[:,i])))
			ax.plot(ndays[nrow-1:], np.cumsum([self.df.values[-1,i]] + list(self.predictions[:,i])), ls='--', label='forecast')
			ax.set_ylabel(self.df.columns[i], fontsize=14)
		axes[-1].set_xlabel('time [days]', fontsize=14)
		plt.legend(frameon=False, fontsize=14)

		if savefile != None:
			plt.savefig(savefile)

		plt.show()
