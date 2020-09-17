import query_EPA_class as q
import time
import os

### Do the main API requests
### Documentation about various parameters and how the call works:
### https://aqs.epa.gov/aqsweb/documents/data_api.html

### Dictionary of parameter names (keys) and tuple of corresponding number and time duration of measurment (value)
PARAM_DICT = {'O3': ('44201', "8-HR RUN AVG BEGIN HOUR"),
			  'CO': ('42101', "8-HR RUN AVG END HOUR"),
			  'SO2': ('42401', "24-HR BLK AVG"),
			  'NO2': ('42602', "1 HOUR"),
			  'PM10': ('81102', "24-HR BLK AVG"),
			  'PM2.5': ('88101', "24-HR BLK AVG"),
			  'Winddirection': ('61104', "1 HOUR"),
			  'Windspeed': ('61103', "1 HOUR"),
			  'Temperature': ('68105', "24 HOUR"),
			  'Pressure': ('68108', "24 HOUR"),
			  'Humidity': ('62201', "1 HOUR")}
### There is a smoke parameter, but it curiously does not return anything when called

### List of list of start and end dates to consider
### The API only allows calls that are 1 Year or shorter in duration
DATE_RANGES = [ ['20160101', '20161231'],
		['20170101', '20171231'],
		['20180101', '20181231'],
		['20190101', '20191231'],
		['20200101', '20201231'] ]

### Parameter names to save as columns in outfile
COLS = ['date_local', 'latitude', 'longitude', 'arithmetic_mean', 'units_of_measure', 'sample_duration']

### Email and key used at signup on AQS
EMAIL = '' ### To be filled in
KEY = '' ### To be filled in

### State id. 06 = California
STATE = '06'



def load_query_to_file(name, num, dtype, date_range):
	print('CURRENT DATES: ', date_range)

	url_params = {'datatype': 'dailyData',
				  'email': EMAIL,
		  		  'key': KEY,
		  		  'param': num,
		  		  'dates': date_range,
		  		  'state': STATE}

	parent_directory = os.path.dirname(os.getcwd())
	file_name = '{}_{}_{}.csv'.format(name, url_params['dates'][0], url_params['dates'][1])
	outfile = os.path.join(
							parent_directory,
							'raw_data',
							file_name)

	print('file name: ' + outfile)


	if os.path.isfile(outfile):
		print("File '{}' already exists! Please delete it and then run this again.".format(outfile))
		#return
	else:
		call = q.Query(url_params)
		call.make_url()
		call.perform_query()
		call.process_query(cols=COLS, outfile=outfile, dtype=dtype)
		time.sleep(10) ### Pause every 10 seconds to limit API calls to < 500 / hr


def run_loop():
	### Loop through parameter names and date ranges, saving csv to outfile
	for name, vals in PARAM_DICT.items():
		num, dtype = vals[0], vals[1]
		print('### CALLING PARAMETER ' + name + ' ###')
		for d in DATE_RANGES:
			load_query_to_file(name=name, num=num, dtype=dtype, date_range=d)


def test_single_query():
	load_query_to_file(
		name='O3',
		num='44201',
		dtype="8-HR RUN AVG BEGIN HOUR",
		date_range=['20160101', '20161231'])



if __name__=='__main__':
	run_loop()
