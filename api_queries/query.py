import numpy as np
import pandas as pd
import requests
import json

class Query():
	'''
	Handle all API queries to EPA AQS service
	https://aqs.epa.gov/aqsweb/documents/data_api.html
	'''

	def __init__(self, url_params):

		self.url_params = url_params

	def make_url(self):
		'''
		Make url for API call based on inputted url_params. Output string
		'''

		self.base_url = "https://aqs.epa.gov/data/api/" + self.url_params['datatype'] \
					+ "/byState?email=" + self.url_params['email'] \
					+ "&key=" + self.url_params['key'] \
					+ "&param=" + self.url_params['param'] \
					+ "&bdate=" + self.url_params['dates'][0] \
					+ "&edate=" + self.url_params['dates'][1] \
					+ "&state=" + self.url_params['state']

	def perform_query(self):
		'''
		Use constructed url to make API call. Output json
		'''

		self.make_url()
		response = requests.get(self.base_url)
		self.json_response = response.json()

	def process_query(self, cols, outfile, dtype="24-HR BLK AVG"):
		'''
		Reformat json from API call by turning into a dataframe and saving as csv to outfile
		INPUTS: cols: array of strings
				outfile: string
				dtype: string
		'''

		df = pd.DataFrame()

		for c in cols:

			try:
				df[c] = [i[c] for i in self.json_response['Data'] if i['sample_duration'] == dtype]
			except KeyError:
				continue

		df = df.reset_index(drop=True)

		df.to_csv(outfile)