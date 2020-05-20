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


# Cleaning Data

def convert_time(time):
    time = int(time)
    return datetime.date.fromtimestamp(time)


df_final = df_final.dropna(subset=['Last_Update'])
df_final['Province_State'].fillna(value='', inplace=True)

df_final["Last_Update"] = df_final["Last_Update"] / 1000
df_final["Last_Update"] = df_final["Last_Update"].apply(convert_time)

print(df_final.head())

# Aggregating data

df_total = df_final.groupby('Country_Region', as_index=False).agg(
    {
        "Confirmed": "sum",
        "Deaths": "sum",
        "Recovered": "sum"
    }
)

# The calculation of daily total of COVID-19 cases at the global level

total_confirmed = df_final["Confirmed"].sum()
total_recovered = df_final["Recovered"].sum()
total_deaths = df_final["Deaths"].sum()

df_top10 = df_total.nlargest(10, "Confirmed")
top10_countries_confirmed = df_top10["Country_Region"].tolist()
top10_confirmed = df_top10["Confirmed"].tolist()

df_top10 = df_total.nlargest(10, "Recovered")
top10_countries_recovered = df_top10["Country_Region"].tolist()
top10_recovered = df_top10["Recovered"].tolist()

df_top10 = df_total.nlargest(10, "Deaths")
top10_countries_deaths = df_top10["Country_Region"].tolist()
top10_deaths = df_top10["Deaths"].tolist()

# Building a dashboard using Python Plotly Subplots
