# AQI Forecasting

## A web-app to forecast the one week air quality index (AQI) based on user location. 

### Requirements

This program works on Anaconda Python v.3.7.6

> conda install --yes python==3.7.6

The following pacakges are also required

> pip insall -r requirements.txt

### Folder Structure

.
+-- requirements.txt
+-- README.md
+-- api_queries
|   +-- query.py
|   +-- run_api.py
+-- figures
+-- forecasting
|   +-- forecast.py
+-- raw_data
+-- states
+-- web_app
|   +-- run_streamlit

### Data

run_api.py - Data come from the EPA Air Quality Service (AQS):

https://aqs.epa.gov/aqsweb/documents/data_api.html

Running run_api.py allows the user to pull data.

### Forecasting

forecast.py - Currently running ARIMA model to forecast O3 concentration:

![O3 2019 Prediction](./figures/o3-2019-prediction.png?raw=true)

### Web-App

run_streamlit.py - Currently only displays a date slider showing a map of California and how the O3 concentration varies with location. Each point represents a monitor from the AWS.