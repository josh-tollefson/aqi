import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import geopandas as gpd
from shapely.geometry import Point, Polygon
import geoplot as gplt
import streamlit as st

@st.cache
def load_data(infile):
	df = pd.read_csv(infile,  usecols=('date_local', 'latitude', 'longitude', 'arithmetic_mean'))
	df.drop_duplicates(inplace=True, ignore_index=True)
	df = df.groupby(['date_local', 'latitude', 'longitude']).mean().reset_index()
	df['date_local'] = pd.to_datetime(df['date_local'])
	return df

@st.cache
def load_map(infile, state='CA'):

	states = gpd.read_file('.\\states\\states.shp')
	return states[states.STATE_ABBR == 'CA']

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mpl.colors.LinearSegmentedColormap('CustomMap', cdict)

def get_colormap(objname,vmax):
    if objname == 'O3':
        cut1 = 0.06 / vmax
        cut2 = 0.076 / vmax
        cut3 = 0.096 / vmax
        cut4 = 0.116 / vmax
        cut5 = 0.375 / vmax
        c = mpl.colors.ColorConverter().to_rgb
        rvb = make_colormap([c('#00e440'), cut1, c('#ffff00'), cut2, c('#ff7e00'), cut3, c('#ff0000'), cut4, c('#8f3f97'), cut5, c('#7e0023')])
        objmap = rvb
    return objmap


infile = '.\\raw_data\\O3_20190101_20191231.csv'
inmap = '.\\states\\states.shp'

processed = load_data(infile)
states_df = load_map(inmap) 

fig, ax = plt.subplots(figsize=(12,12))
ax.set_aspect('equal')
states_df.plot(color='white', edgecolor='black', ax=ax)

date_to_filter = st.slider('date', datetime.date(2019,1,1), datetime.date(2019,12,31))


filtered = processed.loc[processed['date_local'].dt.date == date_to_filter]

geometry = [Point(xy) for xy in zip(filtered['longitude'], filtered['latitude'])]
geo_df = gpd.GeoDataFrame(filtered, geometry=geometry)
import mapclassify as mc


vmin, vmax = 0.0, 0.5
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
cmap = get_colormap('O3', vmax)

gplt.pointplot(
	geo_df,
	hue='arithmetic_mean',
	ax=ax,
	legend=True,
	legend_kwargs={'orientation': 'horizontal'},
	cmap=cmap,
	norm=norm,
    edgecolor='lightgray',
    linewidth=0.5,
    s=10)

st.pyplot()