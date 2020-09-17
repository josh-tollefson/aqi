# AQI Forecasting

## A web-app to forecast the one week air quality index (AQI) based on user location. 

### <ins>Requirements</ins>

pandas
numpy
sklearn
statsmodels
matplotlib
streamlit
requests
json

### <ins>Data</ins>

Data come from the EPA Air Quality Service (AQS):

https://aqs.epa.gov/aqsweb/documents/data_api.html

run_api.py allows the user to pull data.

### <ins>Forecasting</ins>

Currently running ARIMA model to forecast O3 concentration:

![O3 2019 Prediction](./o3-2019-prediction.png?raw=true)
