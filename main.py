import streamlit as st
import geopandas as gpd
import requests
import time  # <-- for the delay
from shapely import Point

#from geolocate import is_location_within_country

st.set_page_config(
    page_title="Border Proximity",
    #page_icon="assets/myicon.png",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

st.title("How Close Am I To The Border?")

# border_dist_flag = st.number_input(
#     label="Enter a border proximity flag (in miles)",
#     min_value=0.0,
#     max_value=1000.0,
#     value=10.0,     # default
#     step=0.5
# )

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

 # Base URL of your deployed API
base_url = "https://borderproximityapi.onrender.com"
# Define endpoint and parameters
endpoint = "/getborderproximity"
params = {"latitude": lat_value, "longitude": lon_value, "country": selected_country}

if isinstance(lat_value, (int, float)) and isinstance(lon_value, (int, float)):
    if st.button("Get Border Proximity"):
        # Send GET request
        with st.spinner("Proximity requested..."):
            time.sleep(0.1)  # slight delay gives Streamlit time to render spinner
            response = requests.get(base_url + endpoint, params=params)

        # Print the result
        if response.status_code == 200:
            # Check if result is not in country
            notInCountry = response.json().get("notincountry")
            errorMessage = response.json().get("error")
            distance_miles = response.json().get("distance_miles")
            distance_km = response.json().get("distance_km")
            map_path_link = response.json().get("map_path_link")
            if errorMessage is not None:
                st.error(f"{errorMessage}")
            elif notInCountry is not None:
                if selected_country == "United States of America":
                    st.error(f"The specified location is not within the **United States** border.")
                else:
                    st.error(f"The specified location is not within the **" + selected_country + "** border.")
            else:
                if selected_country == "United States of America":
                    st.success(f"Object is **{distance_miles}** miles ({distance_km} km) from the closest border of the United States.")
                else:
                    st.success(f"Object is **{distance_miles}** miles ({distance_km} km) from the closest border of {selected_country}.")
                st.markdown(
                    f'<a href="{map_path_link}" target="_blank">Open Path To Border in Maps</a>',
                    unsafe_allow_html=True
                )
        else:
            st.error(f"API error: {response.status_code} - {response.text}")       
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )