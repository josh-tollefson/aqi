# AQI Forecasting

## A web-app to forecast the one week air quality index (AQI) based on user location. 

### <ins>Requirements</ins>

- pandas
- numpy
- sklearn
- statsmodels
- matplotlib
- streamlit
- requests
- json

### <ins>Data</ins>

run_api.py - Data come from the EPA Air Quality Service (AQS):

https://aqs.epa.gov/aqsweb/documents/data_api.html

Running run_api.py allows the user to pull data.

### <ins>Forecasting</ins>

forecast.py - Currently running ARIMA model to forecast O3 concentration:

![O3 2019 Prediction](./figures/o3-2019-prediction.png?raw=true)

### <ins>Web-App</ins>

run_streamlit.py - Currently only displays a date slider showing a map of California and how the O3 concentration varies with location. Each point represents a monitor from the AWS.