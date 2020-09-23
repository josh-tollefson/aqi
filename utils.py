import numpy as np
import geopy
import pandas as pd

def latlon_to_miles(locs):
	'''
	calculate distance in miles between two lat/lon locations
	using the haversine formula
	INPUTS: locs, list of tuples: [(lat1, lon1), (lat2, lon2)]
	OUTPUT: d, float: distance between locs in miles
	'''

	locs = [to_radians(locs[0]), to_radians(locs[1])]
	R = 6371e3 ### Earth's radius in meters

	a = np.power( np.sin( (locs[0][0] - locs[1][0]) / 2 ), 2 ) + \
		np.cos( locs[0][0] ) * np.cos( locs[1][0] ) * np.power( np.sin( (locs[0][1] - locs[1][1]) / 2 ), 2 )

	b = 2 * np.arctan2( np.sqrt(a), np.sqrt(1 - a) )

	d = R * b ### Distance in meters

	return meters_to_miles(d)

def to_radians(loc):

	return (np.radians(loc[0]), np.radians(loc[1]))

def meters_to_miles(d):

	return d * 0.000621371192

def get_zipcode(df):

	geolocator = geopy.Nominatim(user_agent='aqi-query')
	df["Zipcode"] = df.apply(lambda x: geolocator.reverse(str(x["Lat"])+", "+str(x["Lon"])).address.split(",")[-2], axis=1)
	return df


INFILE = '.\\processed_data\\aqs_california_merged_20160101_20200831.csv'
OUTFILE = '.\\processed_data\\aqs_california_merged_zipcode_20160101_20200831.csv'

df_csv = pd.read_csv(INFILE)

locs = [(33.217055, -117.396177), (33.789420, -117.227640)]

print('getting zipcode...')

grouped_df = df_csv.groupby(['Lat','Lon']).size().reset_index()

grouped_df = get_zipcode(grouped_df)

df = pd.merge(df_csv, grouped_df[['Lat', 'Lon', 'Zipcode']], on=['Lat', 'Lon'], how='left')

df.to_csv(OUTFILE, index=False)
