import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
import datetime

# Getting data from Esri dataset's API

raw_data = requests.get("https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases"
                        "/FeatureServer/1/query?where=1%3D1&outFields=*&outSR=4326&f=json")

raw_jason = raw_data.json()
data_frame = pd.DataFrame(raw_jason['features'])

# Transforming Data

data_list = data_frame['attributes'].tolist()
df_final = pd.DataFrame(data_list)
df_final.set_index('OBJECTID')
df_final = df_final[
    ["Country_Region", "Province_State", "Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Last_Update"]]
print(df_final.head())


# Cleaning Data

def convert_time(time):
    time = int(time)
    return datetime.date.fromtimestamp(time)


df_final = df_final.dropna(subset=['Last_Update'])
df_final['Province_State'].fillna(value='', inplace=True)

df_final["Last_Update"] = df_final["Last_Update"] / 1000
df_final["Last_Update"] = df_final["Last_Update"].apply(convert_time)

print(df_final.head())
