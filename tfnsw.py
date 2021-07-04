from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import zipfile
import plotly.express as px
import json

'''
GTFS links:
home: https://gtfs.org/
google reference: https://developers.google.com/transit/gtfs/
source data: https://opendata.transport.nsw.gov.au/dataset/timetables-complete-gtfs/
'''


def get_gtfs_data():
    URL = "https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs"
    API_KEY = 'XXXXXXXXXX'  # masked
    headers = dict(Authorization='apikey ' + API_KEY)
    print("Requesting new GTFS data...")
    response = requests.get(URL, headers=headers)

    # output responses when downloading data
    print("\nstatus code:")
    print(response.status_code)
    print("\nheader:")
    print(response.headers)

    if response:
        print("Request successful, downloading and extracting file")
        open('../gtfs_static.zip', 'wb').write(response.content) # double check directory
        zip = zipfile.ZipFile('../gtfs_static.zip')
        zip.extractall('../')
        return True
    else:
        print("error on the response, no new file added!")
        return False


# download most recent data if needed
# get_gtfs_data()

''' 
expected files:
  agency.txt
  stops.txt
  routes.txt
  calendar.txt
  calendar_dates.txt
  shapes.txt
  trips.txt
  stop_times.txt
  notes.txt
'''

# opening stops.txt
data = pd.read_csv(r'../stops.txt')
stops_df = pd.DataFrame(data)
print(stops_df.head())

stops_df_sample = stops_df.sample(n=200)
bounding_box = (stops_df_sample.stop_lon.min(),   stops_df_sample.stop_lat.max(),      
         stops_df_sample.stop_lat.min(), stops_df_sample.stop_lon.max())

print(bounding_box)

# using plotly, but can try to implement OSM API to get bounded area map and overlay points
fig = px.scatter_geo(stops_df_sample,lat='stop_lat',lon='stop_lon', hover_name="stop_name")
fig.update_layout(title = 'Sample Stops Map - TfNSW', title_x=0.5)
fig.show()




## ------- extra code ----- ##

# df = pd.DataFrame(data, columns = ['mode', 'tap', 'time']) # Alteryx select tool

# print('selected columns')
# # print(df)

# df_train = data[(data['mode'] == 'train') & (data['tap'] == 'off')] # Alteryx filter tool
# print ('selected rows')
# # print(df_train)

# modes = ['lightrail', 'ferry']
# time = ['08:15']
# #df_modes = data(data.mode)
# #df_modes = data(data.isin({'mode':modes, 'time':time}))
# #print ('Additional selected rows')
# #print(df_modes)

# plt.style.use('seaborn-whitegrid')
# fig = plt.figure()
# ax = plt.axes()

# # x = np.linspace(0,10,1000)
# # x = pd.DataFrame(data, columns=['time'])
# # y = np.sin(x)
# # y = pd.DataFrame(data, columns = ['count'])
# # print(type(y))
# # print(y[0:])
# #ax.plot(x, np.sin(x))
# # ax.plot(x[0:], y)

# data.plot(kind='scatter', x = 'time', y = 'count', color = 'red')
# plt.show()
# # fig.savefig('line.png')
