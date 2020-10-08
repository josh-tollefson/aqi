### This is identical to Josh's version but filepaths
# have been updated to support system independence.
# Also the streamlit part has been put into a __main__ function.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
# import geopandas as gpd
# from shapely.geometry import Point, Polygon
# import geoplot as gplt
import streamlit as st
import os

# st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache(allow_output_mutation=True)
def load_data(infile, VARIABLES):
	cols = ['Date', 'Lat', 'Zipcode'] + VARIABLES
	df = pd.read_csv(infile,  usecols=cols)
	df.drop_duplicates(inplace=True, ignore_index=True)
	# df = df.groupby(['Date', 'latitude', 'longitude']).mean().reset_index()
	# df = df.groupby(['Date', 'Zipcode']).mean().reset_index()
	df['Date'] = pd.to_datetime(df['Date'])
	return df

# MAP FUNCTIONS
# @st.cache
# def load_map(infile, state='CA'):
# 	states_file_name = os.path.join(
# 							os.path.dirname(os.getcwd()), # <- this is the parent dir
# 							'states',
# 							'states.shp')
#
# 	states = gpd.read_file(states_file_name)
# 	return states[states.STATE_ABBR == 'CA']

# def make_colormap(seq):
#     """Return a LinearSegmentedColormap
#     seq: a sequence of floats and RGB-tuples. The floats should be increasing
#     and in the interval (0,1).
#     """
#     seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
#     cdict = {'red': [], 'green': [], 'blue': []}
#     for i, item in enumerate(seq):
#         if isinstance(item, float):
#             r1, g1, b1 = seq[i - 1]
#             r2, g2, b2 = seq[i + 1]
#             cdict['red'].append([item, r1, r2])
#             cdict['green'].append([item, g1, g2])
#             cdict['blue'].append([item, b1, b2])
#     return mpl.colors.LinearSegmentedColormap('CustomMap', cdict)
#
# def get_colormap(objname,vmax):
#     if objname == 'O3':
#         cut1 = 0.06 / vmax
#         cut2 = 0.076 / vmax
#         cut3 = 0.096 / vmax
#         cut4 = 0.116 / vmax
#         cut5 = 0.375 / vmax
#         c = mpl.colors.ColorConverter().to_rgb
#         rvb = make_colormap([c('#00e440'), cut1, c('#ffff00'), cut2, c('#ff7e00'), cut3, c('#ff0000'), cut4, c('#8f3f97'), cut5, c('#7e0023')])
#         objmap = rvb
#     return objmap

# LOAD DATA
#infile = '.\\raw_data\\O3_20190101_20191231.csv'
infile = os.path.join(
			os.path.dirname(os.getcwd()), # <- this is the parent dir
			'processed_data',
			'aqs_california_merged_zipcode_20160101_20200831.csv')

VARIABLES = ['O3', 'PM10', 'NO2']
processed = load_data(infile, VARIABLES)
processed['Zipcode'] = processed['Zipcode'].str.strip() # remove whitespace from zipcode data


# USER INTERFACE
st.image('banner.png', use_column_width=True)
st.title("California Air Quality Forecast")
st.subheader('Get real-time, historical, and forecast air quality data for California zipcodes.')

# INPUT DESIRED ZIPCODE
zipcode_option = st.selectbox(
	'Please select the desired zipcode.',
	processed['Zipcode'].value_counts().head().index
)

st.write('You selected:', zipcode_option)

# DESIRED OUTPUT
# output = st.checkbox('Real-time', 'Historical', 'forecast')

button = st.button('Get AQI!')

if button:
	### FORECAST AQI
	# Import forecast file - couldn't get this to work
	import sys
	sys.path.insert(1, os.getcwd() + '../forecasting')
	import forecast
	# import run_forecast


	filtered = processed.loc[processed['Zipcode'] == zipcode_option]
	series = filtered[VARIABLES].fillna(method='bfill').dropna()

	### import forecast module and do multivariate time analysis
	f = forecast.Forecast(series)
	f.get_model()
	f.get_lag()

	# Run Forecast
	f.run_forecast()
	# f.plot_prediction(savefile='../figures/o3-pm2p5-forecast-test.png')





	### PLOT MAP
	# states_df = load_map(inmap)

	# fig, ax = plt.subplots(figsize=(12,12))
	# ax.set_aspect('equal')
	# states_df.plot(color='white', edgecolor='black', ax=ax)

	# date_to_filter = st.slider('Date', datetime.date(2019,1,1), datetime.date(2019,12,31))

	# filtered = processed.loc[processed['date_local'].dt.date == date_to_filter]

	# geometry = [Point(xy) for xy in zip(filtered['longitude'], filtered['latitude'])]
	# geo_df = gpd.GeoDataFrame(filtered, geometry=geometry)
	# import mapclassify as mc

	# vmin, vmax = 0.0, 0.5
	# norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
	# cmap = get_colormap('O3', vmax)
	#
	# gplt.pointplot(
	# 	geo_df,
	# 	hue='arithmetic_mean',
	# 	ax=ax,
	# 	legend=True,
	# 	legend_kwargs={'orientation': 'horizontal'},
	# 	cmap=cmap,
	# 	norm=norm,
	#     edgecolor='lightgray',
	#     linewidth=0.5,
	#     s=10)

	#fig, ax = plt.subplots()

	# st.pyplot()
