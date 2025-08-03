import streamlit as st

def display_results(response, lat, lon):
    if response.status_code == 200:
        # Check if result is not in country
        notInCountry = response.json().get("notincountry")
        locatedCountry = response.json().get("locatedcountry")
        errorMessage = response.json().get("error")
        distance_miles = response.json().get("distance_miles")
        distance_km = response.json().get("distance_km")
        map_path_link = response.json().get("map_path_link")
        if errorMessage is not None:
            st.error(f"{errorMessage}")
        elif notInCountry is not None:
            st.error(f"The specified location is not within the borders of a country. It is likely on a boat or at the bottom of the ocean.")
            error_message = "The specified location is not within the borders of a country. It is likely on a boat or at the bottom of the ocean."
            #border-left: 5px solid #2196F3;
            st.markdown(
                f"""
                <div style="padding: 1em; background-color: #e0f3ff; border-radius: 8px; color: #0b3d91;">
                {error_message}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("&nbsp;") 
            map_path_link = "https://www.google.com/maps?q={},{}".format(lat, lon)
            st.markdown(
                f'<a href="{map_path_link}" target="_blank">Open in Maps</a>',
                unsafe_allow_html=True
            )
        else:
            if locatedCountry == "United States of America":
                st.success(f"Object is **{distance_miles}** miles ({distance_km} km) from the closest border of the United States.")
            else:
                st.success(f"Object is **{distance_miles}** miles ({distance_km} km) from the closest border of {locatedCountry}.")
            st.markdown(
                f'<a href="{map_path_link}" target="_blank">Open Path To Border in Maps</a>',
                unsafe_allow_html=True
            )
    else:
        st.error(f"API error: {response.status_code} - {response.text}")