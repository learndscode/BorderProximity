import geopandas as gpd
from shapely.geometry import Point

def is_location_within_country(lat, lon, country_selected):
    # Path to the downloaded and extracted shapefile
    shapefile_path = "data/ne_110m_admin_0_countries.shp"

    # Load the shapefile
    world = gpd.read_file(shapefile_path)

    point = Point(lon, lat)

    # Select the row(s) where the polygon contains the point
    country = world[world.contains(point)]

    if not country.empty:
        # Compare the NAME column to the expected country name
        return country.iloc[0]['NAME'] == country_selected
    else:
        return False

