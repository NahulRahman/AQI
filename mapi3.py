#This one is the original code byb fahim vai's dowa

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static  # For rendering folium map in Streamlit
import geopandas as gpd

# Google Sheets Public URL (CSV Export)
csv_url = "https://docs.google.com/spreadsheets/d/1aRyCU88momwOk_ONhXXzjbm0-9uoCQrRWVQlQOrTM48/export?format=csv"

# Image paths for each city
image_paths = {
    "All": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\bd.png",
    "Narsingdi": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\narsingdi.png",
    "Dhaka": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\dhaka.png",
    "Chittagong": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\ctg.png",
    "Gazipur": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\gazipur.png",
    "Narayanganj": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\narayanganj.png",
    "Cumilla": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\comilla.png",
    "Rajshahi": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\rajshahi.png",
    "Barishal": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\barisal.png",
    "Savar": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\dhaka.png",
    "Mymensingh": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\mymensingh.png",
    "Rangpur": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\rangpur.png",
    "Khulna": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\khulna.png",
    "Sylhet": "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\sylhet.png",
}







# Station locations for dynamic map
stations = {
    "All": {"lat": 23.685, "lon": 90.3563, "zoom": 7},
    "Dhaka": {"lat": 23.7779, "lon": 90.3762, "zoom": 12},
    "Chittagong": {"lat": 22.3644, "lon": 91.8045, "zoom": 12},
    "Gazipur": {"lat": 23.9914, "lon": 90.3541, "zoom": 12},
    "Narayanganj": {"lat": 23.6238, "lon": 90.5072, "zoom": 12},
    "Sylhet": {"lat": 24.8949, "lon": 91.8687, "zoom": 12},
    "Khulna": {"lat": 22.8457, "lon": 89.5627, "zoom": 12},
    "Rajshahi": {"lat": 24.3833, "lon": 88.6033, "zoom": 12},
    "Barishal": {"lat": 22.701, "lon": 90.3541, "zoom": 12},
    "Savar": {"lat": 23.8583, "lon": 90.2667, "zoom": 12},
    "Mymensingh": {"lat": 24.7471, "lon": 90.4203, "zoom": 12},
    "Rangpur": {"lat": 25.7439, "lon": 89.2752, "zoom": 12},
    "Cumilla": {"lat": 23.4607, "lon": 91.1809, "zoom": 12},
    "Narsingdi": {"lat": 23.7924, "lon": 90.7189, "zoom": 12},
}

# Function to create a dynamic map
def create_dynamic_map(selected_city):
    city_info = stations.get(selected_city, stations["All"])
    lat, lon, zoom = city_info["lat"], city_info["lon"], city_info["zoom"]

    m = folium.Map(location=[lat, lon], zoom_start=zoom)

    if selected_city == "All":
        marker_cluster = MarkerCluster().add_to(m)
        for station, info in stations.items():
            if station != "All":
                folium.Marker(
                    location=[info["lat"], info["lon"]],
                    popup=station,
                    icon=folium.Icon(color="blue"),
                ).add_to(marker_cluster)
    else:
        folium.Marker(
            location=[lat, lon],
            popup=f"{selected_city} (AQI Station)",
            icon=folium.Icon(color="red"),
        ).add_to(m)

    return m













# Load dataset from Google Sheets
@st.cache_data
def load_data_from_gsheets():
    return pd.read_csv(csv_url)







# Preprocess Dataset
def preprocess_data(df):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    city_corrections = {
        "Narsingdi": ["Norshindi", "Narshindi", "Narsindi"],
        "Chittagong": ["Chittgong", "Chattogram"],
        "Narayanganj": ["Narayangonj"],
        "Barishal": ["Barisal"],
    }
    for correct_city, wrong_cities in city_corrections.items():
        df["City"] = df["City"].replace(wrong_cities, correct_city)

    df = df[df["AQI"].notna()]
    df = df[df["AQI"] != "DNA"]
    df["AQI"] = pd.to_numeric(df["AQI"], errors="coerce")
    df = df.sort_values(by="Date", ascending=True)
    return df

# Load and preprocess the data
raw_data = load_data_from_gsheets()
preprocessed_df = preprocess_data(raw_data)

# Enforce specific order for cities
city_order = [
    "All", "Dhaka", "Chittagong", "Gazipur", "Narayanganj", "Sylhet", "Khulna",
    "Rajshahi", "Barishal", "Savar", "Mymensingh", "Rangpur", "Cumilla", "Narsingdi",
]









# Streamlit UI
st.title("Welcome to AQI Website")

selected_city = st.selectbox("Select Your City", city_order)

st.subheader(f"Map of {selected_city}")
dynamic_map = create_dynamic_map(selected_city)
folium_static(dynamic_map)

map_path = image_paths.get(selected_city, "C:\\Users\\Acer\\Downloads\\paper\\fahim_vai\\maps\\bd.png")
st.image(map_path, caption=f"Map of {selected_city}", use_container_width=True)

if selected_city == "All":
    filtered_df = preprocessed_df
else:
    filtered_df = preprocessed_df[preprocessed_df["City"] == selected_city]

st.subheader(f"AQI Trend for {selected_city}")
plt.figure(figsize=(12, 6))

if selected_city == "All":
    cities = preprocessed_df["City"].unique()
    for city in cities:
        city_data = preprocessed_df[preprocessed_df["City"] == city]
        plt.plot(city_data["Date"], city_data["AQI"], label=city)
else:
    plt.plot(filtered_df["Date"], filtered_df["AQI"], label=selected_city, color="blue", marker="o")

plt.title(f"AQI Trends Over Time ({selected_city})")
plt.xlabel("Date")
plt.ylabel("AQI")
plt.legend(loc="upper right")
plt.grid(True)
plt.xticks(rotation=45)

st.pyplot(plt)

st.subheader(f"Dataset for {selected_city}")
st.dataframe(filtered_df, hide_index=True)







##Dialog Box
import streamlit as st

# Initialize session state to manage the dialog box visibility
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False

# Function to display the dialog box
def show_dialog():
    with st.container():
        st.markdown("### Subscribe to Alerts")
        st.write("Enter your details to subscribe.")
        
        # Email input
        email = st.text_input("Enter your email:")
        
        # City selection dropdown with a unique key
        city_order = [
            "All", "Dhaka", "Chittagong", "Gazipur", "Narayanganj", "Sylhet", "Khulna", 
            "Rajshahi", "Barishal", "Savar", "Mymensingh", "Rangpur", "Cumilla", "Narsingdi"
        ]
        unique_key = "city_selectbox"  # Add a unique key here
        selected_city = st.selectbox("Select Your City", city_order, key=unique_key)
        
        # Buttons for "Submit" and "Close"
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit"):
                # Handle subscription logic here (e.g., save email and city)
                st.session_state.show_dialog = False
                st.success(f"Subscription successful! Email: {email}, City: {selected_city}")
                st.experimental_rerun()
        with col2:
            if st.button("Close"):
                st.session_state.show_dialog = False
                st.experimental_rerun()

# Main page
st.title("Welcome to the Alert Subscription Page")

# Button to show the dialog box
if st.button("Subscribe for free to get alert message"):
    st.session_state.show_dialog = True

# Display the dialog box if the state is set to True
if st.session_state.show_dialog:
    show_dialog()




