import streamlit as st
import geopandas as gpd
import requests
import time  # <-- for the delay

from shapely import Point
from displayResult import display_results

st.set_page_config(
    page_title="Border Proximity",
    #page_icon="assets/myicon.png",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

st.title("How close is the Object to the Border?")

call_api = False  # Initialize the results state
show_api = False  # Initialize the button state

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
#shapefile_path = "data/ne_110m_admin_0_countries.shp"

# Load the shapefile
#world = gpd.read_file(shapefile_path)

# Extract sorted list of country names
#country_list = sorted(world['NAME'].unique())

# Create countries dropdown
#default = 'United States of America'

#selected_country = st.selectbox("Select a country", country_list, index=country_list.index(default))

# Base URL of your deployed API
base_url = "https://borderproximityapi.onrender.com"
# Define endpoint and parameters
endpoint = "/getborderproximity"
params = {"latitude": lat_value, "longitude": lon_value}

# Create columns: [left spacer, col1, tiny spacer, col2, right spacer]
butcol1, butcol2, spacer_right = st.columns([1, 3, 1])

if isinstance(lat_value, (int, float)) and isinstance(lon_value, (int, float)):
    with butcol1:
        if st.button("Get Border Proximity"):
            show_api = False  # Reset the button state
            call_api = True        
    with butcol2:
        if st.button("Show border proximity API call"):
            call_api = False  # Reset the results state    
            show_api = True
    
    # Display results if the API call was successful
    if call_api:
        # Send GET request
        with st.spinner("Proximity requested..."):
            time.sleep(0.1)  # slight delay gives Streamlit time to render spinner
            response = requests.get(base_url + endpoint, params=params)
            display_results(response)
    if show_api:
        #st.markdown("---")  # Optional horizontal rule       
        st.write(f"API Call: `{base_url + endpoint}?latitude={lat_value}&longitude={lon_value}`")
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )