# AQI Forecasting

## A web-app to forecast the one week air quality index (AQI) based on user location. 

### Requirements

This program works on Anaconda Python v.3.7.6

> conda install --yes python==3.7.6

The following pacakges are also required

> pip install -r requirements.txt

### Folder Structure

```
aqi
|   requirements.txt
|   README.md
|
|___api_queries
    |   query.py
    |   run_api.py
|   figures
|___forecasting
    |   forecast.py
    |   run_forecast.py
|   raw_data
|   states
|___web_app
    |   run_streamlit.py
```

### Data

run_api.py - Data come from the EPA Air Quality Service (AQS):

https://aqs.epa.gov/aqsweb/documents/data_api.html

Running run_api.py allows the user to pull data.

### Forecasting

forecasting - Run ARIMA model to forecast O3 concentration:

![O3 2019 Prediction](./figures/o3-2019-prediction.png?raw=true)

Also runs multivarite time-series forecasting with VAR; 7-day forecast of O3 concentration and Temperature:

![O3 Temp_2019 Prediction](./figures/o3-temp-forecast.png?raw=true)

### Web-App

run_streamlit.py - Currently only displays a date slider showing a map of California and how the O3 concentration varies with location. Each point represents a monitor from the AQS.
