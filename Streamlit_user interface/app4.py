# Description: Streamlit app for unified search using FastAPI backend
import streamlit as st
import httpx  # To send requests to the FastAPI backend
import pandas as pd  # For displaying search results in a DataFrame
import folium
from streamlit_folium import st_folium

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/unified_search"

# Helper function to create a Folium map
def create_folium_map(center, zoom_start=8):
    m = folium.Map(location=center, zoom_start=zoom_start)

    # Add an interactive feature to select a location
    folium.Marker(
        location=center,
        draggable=True,
        icon=folium.Icon(color="red"),
        tooltip="Central Point",
    ).add_to(m)

    return m

# Generate popup content for markers
def popupStr_generator(df_row):
    try:
        popup_content = []

        # Add name if available
        if df_row.get("name") and df_row["name"] != "N/A":
            popup_content.append(f"<b>{df_row['name']}</b><br>")

        # Add amenity if available
        if df_row.get("amenity") and df_row["amenity"] != "N/A":
            popup_content.append(f"<i>Amenity:</i> {df_row['amenity']}<br>")

        # Add link if available
        if df_row.get("sameAs") and df_row["sameAs"] != "N/A":
            popup_content.append(f"<i>Link:</i> <a href='{df_row['sameAs']}'>{df_row['sameAs']}</a><br>")

        # Add telephone if available
        if df_row.get("telephone") and df_row["telephone"] != "N/A":
            popup_content.append(f"<i>Telephone:</i> {df_row['telephone']}<br>")

        # Add address if available
        if df_row.get("address") and isinstance(df_row["address"], dict):
            address = df_row["address"]
            street = address.get("streetAddress", "")
            postal_code = address.get("postalCode", "")
            locality = address.get("addressLocality", "")
            full_address = ", ".join(filter(None, [street, postal_code, locality]))
            if full_address:
                popup_content.append(f"<i>Address:</i> {full_address}<br>")

        # Add Landkreis or Stadt if available
        if df_row.get("Landkreis") and df_row["Landkreis"] != "N/A":
            popup_content.append(f"<b>{df_row['Landkreis']}</b><br>")
        elif df_row.get("Stadt") and df_row["Stadt"] != "N/A":
            popup_content.append(f"<b>{df_row['Stadt']}</b><br>")

        # Add postcode if available
        if df_row.get("PLZ") and df_row["PLZ"] != "N/A":
            popup_content.append(f"<i>Postcode:</i> {df_row['PLZ']}<br>")

        # Add event type if available
        if df_row.get("categories") and isinstance(df_row["categories"], list):
            event_type = df_row["categories"]
            separator = ", "
            event_cat = separator.join(event_type)  # Combine all event types into a single string
            popup_content.append(f"<i>Event Type:</i> {event_cat}<br>")

        # Add average rent if available
        if df_row.get("average_rent") and df_row["average_rent"] != "N/A":
            popup_content.append(f"<i>Rent:</i> {df_row['average_rent']}€ per m²<br>")

        return "".join(popup_content).strip()
    except Exception as e:
        print(f"Error in popupStr_generator: {e}")
        return ""

# Function to normalize columns with mixed types
def normalize_column(df, column_name):
    # If the column contains lists, we convert them to strings or take the first item if needed
    if column_name in df:
        df[column_name] = df[column_name].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else str(x) if x is not None else ""
        )
    return df

# Main Streamlit app function
def main():
    st.title("KielAI Lab")

    # Sidebar for user inputs
    st.sidebar.header("Search Parameters")

    # Query input field (text)
    query = st.sidebar.text_input("Search Query (e.g., restaurant, park)", key="query_input")
    rent = st.sidebar.checkbox("Looking for rent price?", value=False)
    
    # Dropdown for area type (radius or polygon)
    area_type = st.sidebar.selectbox("Select Area Type", ["Radius", "Polygon"], key="area_type_select")

    # Input field for radius if selected
    radius = None
    if area_type == "Radius":
        radius = st.sidebar.number_input("Radius (in km)", value=0.0, min_value=0.0, key="radius_input")
    
    # Time parameter
    time = st.sidebar.text_input("Time (e.g., today, Sunday, 2023-12-11)", key="time_input")

    # Default center location (e.g., Kiel)
    if "selected_coords" not in st.session_state:
        st.session_state.selected_coords = [54.2194, 9.6961]  # Kiel coordinates

    center = st.session_state.selected_coords

    # Initialize session state for search results
    if "search_results" not in st.session_state:
        st.session_state.search_results = []

    # Initialize session state for DataFrame
    if "results_df" not in st.session_state:
        st.session_state.results_df = pd.DataFrame()  # Empty DataFrame

    # Search button
    if st.sidebar.button("Search", key="search_button"):
        # Reset the selected coordinates to the center (for a new search)
        st.session_state.selected_coords = center

        # Build the query dictionary
        query_dict = {}
        if query:
            query_dict["what"] = query.split(",")
        if time:
            query_dict["time"] = time
        if rent:
            query_dict["rent"] = True

        # Prepare the payload
        payload = {
            "query": query_dict,
            "point": [center[0], center[1]],  # Use center coordinates for the search
            "area": radius if area_type == "Radius" else "polygon",
        }

        # Send request to FastAPI
        try:
            with st.spinner("Searching..."):
                response = httpx.post(BACKEND_URL, json=payload)
                response.raise_for_status()

                # Process the response
                data = response.json()
                results = data.get("results", [])
                num_results = data.get("num_results", 0)

                # Update session state with new results
                st.session_state.search_results = results
                st.session_state.results_df = pd.DataFrame(results)

                # Normalize the 'Landkreis' and 'Stadtteil' columns to avoid Arrow serialization issues
                st.session_state.results_df = normalize_column(st.session_state.results_df, "Landkreis")
                st.session_state.results_df = normalize_column(st.session_state.results_df, "Stadtteil")

                st.success(f"Found {num_results} results!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Create the map with the selected coordinates
    m = create_folium_map(center=center)

    # Add search results to the map
    for result in st.session_state.search_results:
        try:
            popup_content = popupStr_generator(result)
            folium.Marker(
                location=[result["lat"], result["lon"]],
                popup=popup_content,
                tooltip=result.get("name", "Click for details"),
                icon=folium.Icon(color="blue"),
            ).add_to(m)
        except KeyError:
            continue  # Skip if lat/lon are missing

    # Display the map and capture click events
    map_data = st_folium(m, width=700, height=500, key="map")

    # Update selected coordinates when the map is clicked
    if map_data is not None and "last_clicked" in map_data and map_data["last_clicked"] is not None:
        st.session_state.selected_coords = [
            map_data["last_clicked"]["lat"],
            map_data["last_clicked"]["lng"],
        ]

    selected_lat, selected_lon = st.session_state.selected_coords
    st.sidebar.markdown(f"Selected Location:\nLat: {selected_lat:.4f}, Lon: {selected_lon:.4f}")

    # Display the results DataFrame
    if not st.session_state.results_df.empty:
        st.write("## Results:")
        st.dataframe(st.session_state.results_df)

if __name__ == "__main__":
   main()