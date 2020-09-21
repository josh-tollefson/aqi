import numpy as np
import pandas as pd
import os
import glob
from functools import reduce
import logging
import matplotlib.pyplot as plt

def load_data(infile, variable):

	try:
		df = pd.read_csv(infile,  usecols=('date_local', 'latitude', 'longitude', 'arithmetic_mean'))
		df.drop_duplicates(inplace=True, ignore_index=True)
		df = df.groupby(['date_local', 'latitude', 'longitude']).mean().reset_index()
		df['date_local'] = pd.to_datetime(df['date_local'])
		df.rename(columns={'arithmetic_mean': variable, 'date_local': 'Date', 'longitude': 'Lon', 'latitude': 'Lat'}, inplace=True)
		return df

	except ValueError: ### csv file is empty and does not contain column names for usecols
		logging.warning('csv file: ' + infile + ' does not contain correct column names. Is it empty?')
		return None


def combine_files(VARIABLES, OUTFILE):

	data_frames = []

	parent_directory = os.path.dirname(os.getcwd())
	inpath = os.path.join(parent_directory, 'raw_data')
	outcsv = os.path.join(parent_directory, 'processed_data', OUTFILE)

	for v in VARIABLES:

		df_same_var = pd.DataFrame()

		for file in glob.glob(os.path.join(inpath, v + '*.csv')):

			df = load_data(file, v)

			if df is not None:

				df_same_var = df_same_var.append(df, ignore_index=True)

		data_frames.append(df_same_var.copy())
		del df_same_var

	df_merged = reduce(lambda left,right: pd.merge(left,right,on=['Date', 'Lat', 'Lon'], how='outer'), data_frames).sort_values(by=['Date', 'Lat']).reset_index(drop=True)

	df_merged.to_csv(outcsv, index=False)


###############
# User Inputs #
###############

VARIABLES = ['O3', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'Temperature', 'Pressure', 'Humidity', 'Windspeed', 'Winddirection']

OUTFILE = 'aqs_california_merged_20160101_20200831.csv'

###############

if __name__ == '__main__':

	combine_files(VARIABLES, OUTFILE)