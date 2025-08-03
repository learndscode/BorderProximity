import streamlit as st

def display_results(response, selected_country):
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
            if selected_country == "United States of America":
                st.error(f"The specified location is not within the **United States&#39;s** borders. It is located in {locatedCountry}.")
            else:
                if locatedCountry == "United States of America":
                    st.error(f"The specified location is not within **{selected_country}&#39;s** borders. It is located in the United States.")
                else:
                    st.error(f"The specified location is not within **{selected_country}&#39;s** borders. It is located in {locatedCountry}.")
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