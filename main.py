import streamlit as st
import pandas as pd
import geopandas as gpd
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

# Set zoom level
zoom_level = 10


# Path to the downloaded and extracted shapefile
shapefile_path = "data/ne_110m_admin_0_countries.shp"

# Load the shapefile
world = gpd.read_file(shapefile_path)
# Reproject to World Mercator (EPSG:3395)
world = world.to_crs(epsg=3395)

# Extract sorted list of country names
country_list = sorted(world['NAME'].unique())

# Create countries dropdown
default = 'United States of America'

selected_country = st.selectbox("Select a country", country_list, index=country_list.index(default))

if isinstance(lat_value, (int, float)) and isinstance(lon_value, (int, float)):
    if is_location_within_country(lat_value, lon_value, selected_country):
        # Create a lat/long point
        location = Point(lon_value, lat_value)

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
            #Distance in miles
            distance_to_border_miles = distance_to_border_meters / 1609.344
            distance_to_border_km = distance_to_border_meters / 1000

            # Get closest border point
            boundary = target_country.geometry.iloc[0].boundary
            closest_point = boundary.interpolate(boundary.project(projected_point))
            # Convert back to lat/lon
            closest_point_latlon = gpd.GeoSeries([closest_point], crs=world.crs).to_crs(epsg=4326).iloc[0]
            
            closest_lat_txt = str(round(closest_point_latlon.y, 2))
            closest_lon_txt = str(round(closest_point_latlon.x, 2))

            if selected_country == "United States of America":
                selected_country_txt = "United States"
            else:
                selected_country_txt = selected_country

            if distance_to_border_miles > border_dist_flag:
                st.write("Object is **" + str(round(distance_to_border_miles, 1)) + " miles (" + str(round(distance_to_border_km, 1)) + " km)** from the nearest " + selected_country_txt + " border (" + closest_lat_txt + ", " + closest_lon_txt + ").")
            else: 
                dist_to_bord = str(round(distance_to_border_miles, 1))
                dist_to_bord_km = str(round(distance_to_border_km, 1))
                st.markdown(
                    f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Object is **{dist_to_bord} miles ({dist_to_bord_km} km)** from the nearest {selected_country_txt} border ({closest_lat_txt} , {closest_lon_txt}).</span>",
                    unsafe_allow_html=True
                )
            # Publish link to Google Maps
            st.markdown(
                f'<a href="https://www.google.com/maps/search/?api=1&query={lat_value},{lon_value}&zoom={zoom_level}" target="_blank">Open Object&#39;s Location in Maps</a>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<a href="https://www.google.com/maps/dir/{lat_value},{lon_value}/{closest_lat_txt},{closest_lon_txt}" target="_blank">Open Path To Border in Maps</a>',
                unsafe_allow_html=True
            )
            
    else:
        st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Object is **NOT** inside **{selected_country}**</span>",
            unsafe_allow_html=True
        )
        # Publish object's location link to Google Maps
        st.markdown(
            f'<a href="https://www.google.com/maps/search/?api=1&query={lat_value},{lon_value}&zoom={zoom_level}" target="_blank">Open Object&#39;s Location in Maps</a>',
            unsafe_allow_html=True
        )
    
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )