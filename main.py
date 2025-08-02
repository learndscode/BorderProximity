import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

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
    max_value=20.0,
    value=10.0,     # default
    step=0.5
)

# Get longitude and latitude coordinates
lat_value = st.number_input(
    label="Enter a Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=32.7767,     # default
    step=1.0
)

long_value = st.number_input(
    label="Enter a Latitude",
    min_value=-180.0,
    max_value=180.0,
    value=-96.797,     # default
    step=1.0
)

# Path to the downloaded and extracted shapefile
shapefile_path = "data/ne_110m_admin_0_countries.shp"

# Load the shapefile
world = gpd.read_file(shapefile_path)
# Reproject to World Mercator (EPSG:3395)
world = world.to_crs(epsg=3395)

# Extract sorted list of country names
country_list = sorted(world['NAME'].unique())

# Create Streamlit dropdown
selected_country = st.selectbox("Select a country", country_list)

if isinstance(lat_value, (int, float)) and isinstance(long_value, (int, float)):
    if is_location_within_country(lat_value, long_value, selected_country):
        # Create a lat/long point
        location = Point(long_value, lat_value)

        # Reproject point to the same CRS
        location_gdf = gpd.GeoSeries([location], crs="EPSG:4326").to_crs(epsg=3395)
        projected_point = location_gdf.iloc[0]

        # Get the country geometry
        target_country = world[world['NAME'] == selected_country]

        if target_country.empty:
            #raise ValueError("Country not found in shapefile.")
            st.markdown(
                f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>ERROR: Could not find country in earth file.</span>",
                unsafe_allow_html=True
            )
        else:
            # Distance in meters
            distance_to_border_meters = projected_point.distance(target_country.geometry.iloc[0].boundary)
            distance_to_border_miles = distance_to_border_meters / 1609.344

            if distance_to_border_miles > border_dist_flag:
                st.write("Object is **" + str(round(distance_to_border_miles, 1)) + " miles** from the nearest " + selected_country + " border.")
            else: 
                dist_to_bord = str(round(distance_to_border_miles, 1))
                st.markdown(
                    f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Object is **{dist_to_bord}** miles from the nearest {selected_country} border.</span>",
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Object is **NOT** inside **{selected_country}**</span>",
            unsafe_allow_html=True
        )
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )