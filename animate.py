import numpy as np
import netCDF4

from bokeh.client import push_session
from bokeh.io import curdoc
from bokeh.plotting import vplot, hplot

from viz import climate_map, timeseries, legend, get_slice  

# Data
data = netCDF4.Dataset('data/Land_and_Ocean_LatLong1.nc')
t = data.variables['temperature']

# Plots
climate_map = climate_map()
timeseries = timeseries()
legend = legend()

# Create layout
map_legend = hplot(climate_map, legend)
layout = vplot(map_legend, timeseries)

# open a session to keep our local document in sync with server
session = push_session(curdoc())

# Select data source for climate_map
renderer = climate_map.select(dict(name="image"))
ds = renderer[0].data_source

def update():
   for year_index in np.arange(2000, 2015, 1):
        for month_index in np.arange(1, 13, 1):
            image = get_slice(t, year_index, month_index)
            ds.data["image"] = [image]

curdoc().add_periodic_callback(update, 20)

session.show() # open the document in a browser

session.loop_until_closed() # run forever
