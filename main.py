import streamlit as st
import pandas as pd
import geopandas as gpd
import requests
from shapely import Point

from geolocate import is_location_within_country

st.set_page_config(
    page_title="Border Proximity",
    #page_icon="assets/myicon.png",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

st.title("How Close Am I To The Border?")

border_dist_flag = st.number_input(
    label="Enter a border proximity flag (in miles)",
    min_value=0.0,
    max_value=1000.0,
    value=10.0,     # default
    step=0.5
)

# Get longitude and latitude coordinates
lat_value = st.number_input(
    label="Enter Object's Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=32.7767,     # default
    step=1.0
)

lon_value = st.number_input(
    label="Enter Object's Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=-96.797,     # default
    step=1.0
)

# Path to the downloaded and extracted shapefile
shapefile_path = "data/ne_110m_admin_0_countries.shp"

# Load the shapefile
world = gpd.read_file(shapefile_path)

# Extract sorted list of country names
country_list = sorted(world['NAME'].unique())

# Create countries dropdown
default = 'United States of America'

selected_country = st.selectbox("Select a country", country_list, index=country_list.index(default))

if isinstance(lat_value, (int, float)) and isinstance(lon_value, (int, float)):
    # Base URL of your deployed API
    base_url = "https://borderproximityapi.onrender.com"
    # Define endpoint and parameters
    endpoint = "/getborderproximity"
    params = {"latitude": lat_value, "longitude": lon_value, "country": selected_country}

    # Send GET request
    response = requests.get(base_url + endpoint, params=params)

    # Print the result
    if response.status_code == 200:
        print(response.json())  # e.g., {'result': 8}
    else:
        print(f"Error: {response.status_code}, {response.text}")
    
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )