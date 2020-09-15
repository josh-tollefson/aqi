import numpy as np
import pandas as pd
import requests
import json
import time

class Query():

	def __init__(self, url_params):

		self.url_params = url_params

	def make_url(self):

		self.base_url = "https://aqs.epa.gov/data/api/" + self.url_params['datatype'] \
					+ "/byState?email=" + self.url_params['email'] \
					+ "&key=" + self.url_params['key'] \
					+ "&param=" + self.url_params['param'] \
					+ "&bdate=" + self.url_params['dates'][0] \
					+ "&edate=" + self.url_params['dates'][1] \
					+ "&state=" + self.url_params['state']

	def perform_query(self):

		self.make_url()
		response = requests.get(self.base_url)
		self.json_response = response.json()

	def process_query(self, cols, outfile, dtype=["24-HR BLK AVG"]):

		df = pd.DataFrame()

		for c in cols:

			for d in dtype:
				try:
					df[c] = [i[c] for i in self.json_response['Data'] if i['sample_duration'] == dtype]
				except KeyError:
					continue

		df = df.reset_index(drop=True)

		df.to_csv(outfile)