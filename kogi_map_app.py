import streamlit as st
import pydeck as pdk
import pandas as pd
import json


# Title for the app
st.title("Connectivity in Benue and Taraba States")

# Includes logo of Notify Health
st.logo('https://static.wixstatic.com/media/8f90d6_882dbd58c7884c1ea5ad885d809f03ac~mv2.png/v1/fill/w_479,h_182,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Notify%20Health%20Logo%20Blue.png',
        link="https://www.notifyhealth.org/",
        icon_image='https://static.wixstatic.com/media/8f90d6_882dbd58c7884c1ea5ad885d809f03ac~mv2.png/v1/fill/w_479,h_182,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Notify%20Health%20Logo%20Blue.png'
        )


###### LOAD DATA ######

# Cities data with two dots per city
cities_data = [
    # Base black dots
    {"state": "Benue","city": "Makurdi", "lat": 7.7306, "lon": 8.5300, "color": [0, 0, 0], "radius": 3000, "elevation": 0},
    {"state": "Benue","city": "Gboko", "lat": 7.3167, "lon": 9.0000, "color": [0, 0, 0], "radius": 3000, "elevation": 0},
    {"state": "Taraba","city": "Wukari", "lat": 7.8500, "lon": 9.7833, "color": [0, 0, 0], "radius": 3000, "elevation": 0},
    {"state": "Taraba","city": "Jalingo", "lat": 8.9000, "lon": 11.3667, "color": [0, 0, 0], "radius": 3000, "elevation": 0},
    {"state": "Taraba","city": "Gembu", "lat": 6.7000, "lon": 11.2667, "color": [0, 0, 0], "radius": 3000, "elevation": 0},
    {"state": "Kogi","city": "Anyigba", "lat": 7.4958, "lon": 7.1889, "color": [0, 0, 0], "radius": 3000, "elevation": 0},
    {"state": "Kogi","city": "Lokoja", "lat": 7.8000, "lon": 6.7333, "color": [0, 0, 0], "radius": 3000, "elevation": 0},


    # Top red dots
    {"state": "Benue","city": "Makurdi", "lat": 7.7306, "lon": 8.5300, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
    {"state": "Benue","city": "Gboko", "lat": 7.3167, "lon": 9.0000, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
    {"state": "Taraba","city": "Wukari", "lat": 7.8500, "lon": 9.7833, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
    {"state": "Taraba","city": "Gembu", "lat": 6.7000, "lon": 11.2667, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
    {"state": "Taraba","city": "Jalingo", "lat": 8.9000, "lon": 11.3667, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
    {"state": "Kogi","city": "Anyigba", "lat": 7.4958, "lon": 7.1889, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
    {"state": "Kogi","city": "Lokoja", "lat": 7.8000, "lon": 6.7333, "color": [255, 0, 0], "radius": 1500, "elevation": 1},
]

# Create DataFrame for Main cities
cities_df = pd.DataFrame(cities_data)

# Load data for benue health centers
csv_benue = "BENUE-PRIMARY HEALTH CENTERS-data - BENUE-PRIMARY HEALTH CENTERS-data.csv"
df_benue_health_centers = pd.read_csv(csv_benue)
# Filter operational health centers
benue_operational_health_centers = df_benue_health_centers[df_benue_health_centers["is_operational"] == True]
count_health_centers_per_lga_benue = benue_operational_health_centers.groupby("lga").size().reset_index(name="operational_facility_count").sort_values(by="operational_facility_count", ascending=False)

# Load data for taraba health centers
csv_taraba = "TARABA-PRIMARY HEALTH CENTERS-data - TARABA-PRIMARY HEALTH CENTERS-data.csv"
df_taraba_health_centers = pd.read_csv(csv_taraba)
# Filter operational health centers
taraba_operational_health_centers = df_taraba_health_centers[df_taraba_health_centers["is_operational"] == True]
count_health_centers_per_lga_tar = taraba_operational_health_centers.groupby("lga").size().reset_index(name="operational_facility_count").sort_values(by="operational_facility_count", ascending=False)

st.dataframe(count_health_centers_per_lga_benue)
st.dataframe(count_health_centers_per_lga_tar)

# @st.cache_data
# def load_data(url):
#     return pd.read_csv(url)

# Load data for population 

##### Benue LGA population projections (2025) ##### 
data_population_benue = {
    "Local Government Area": [
        "Ado", "Agatu", "Apa", "Buruku", "Gboko", "Guma", "Gwer East", "GwerWest",
        "Katsina (Benue)", "Konshish", "Kwande", "Logo", "Makurdi", "Obi", "Ogbadibo",
        "Ohimini", "Oju", "Okpokwu", "Oturkpo", "Tarka", "Ukum", "Ushongo", "Vandeiky"
    ],
    "Total Population": [
        286476, 179743, 150425, 320562, 561818, 301785, 262273, 190366, 351086, 352682,
        387228, 264252, 467431, 153523, 203851, 110141, 262058, 272936, 414489, 123429,
        337512, 298528, 365932
    ]
}

# Age group percentages
age_group_percentages = {
    "0–14": 0.392,
    "15–24": 0.181,
    "25–54": 0.332,
    "55+": 0.094
}

# Convert to DataFrame
df_population_benue = pd.DataFrame(data_population_benue)

# Calculate age group populations
for group, pct in age_group_percentages.items():
    df_population_benue[group] = (df_population_benue["Total Population"] * pct).round(0).astype(int)


##### Taraba LGA population projections (2025) ##### 
data_population_taraba = {
    "Local Government Area": [
        "Ardo-Kola", "Bali", "Disputed Areas", "Donga", "Gashaka", "Gassol", "Ibi",
        "Jalingo", "Karim-La", "Kurmi", "Lau", "Sardauna", "Takum", "Ussa", "Wukari", "Yorro", "Zing"
    ],
    "Total Population": [
        150400, 361600, 34200, 228000, 149300, 419600, 144300,
        240300, 332200, 156300, 162900, 384000, 230300, 155800, 406900, 154100, 218600
    ]
}

# Age group percentages (updated)
age_group_percentages_taraba = {
    "0–14": 0.417,
    "15–64": 0.549,
    "65+": 0.033
}

# Convert to DataFrame
df_population_taraba = pd.DataFrame(data_population_taraba)

# Calculate age group populations
for group, pct in age_group_percentages_taraba.items():
    df_population_taraba[group] = (df_population_taraba["Total Population"] * pct).round(0).astype(int)

# Load your GeoJSON
# with open("nigeria_Local_Government_Area_level_2.geojson") as f:
#     geojson_data = json.load(f)

# Find maximum population in your data for scaling
max_population = max(
    df_population_benue["Total Population"].max(), 
    df_population_taraba["Total Population"].max()
)

# Load GeoJSON with Nigeria's States
with open("nigeria-states.geojson") as f:
    states_geojson_data = json.load(f)

# Load GeoJSON with Nigeria's Local Government Areas (LGAs)
with open("nigeria_lga.geojson") as f:
    geojson_data = json.load(f)

# Map population values to features only for Benue, Kogi, Taraba
for feature in geojson_data["features"]:
    state_name = feature["properties"]["state"]
    lga_name = feature["properties"]["lga"]
    
    # Filter to only the desired states
    # Only work with Benue, Kogi, Taraba
    if state_name in ["Benue", "Kogi", "Taraba"]:
        population = 0
        age_0_14 = 0
        count_health_centers = 0
        # Match on uppercase LGA name
        lga_name_upper = lga_name.upper()

        # Check Benue
        match_benue = df_population_benue[df_population_benue["Local Government Area"] == lga_name]
        if not match_benue.empty:
            population = int(match_benue["Total Population"].values[0])
            age_0_14 = int(match_benue["0–14"].values[0])

        # Check Taraba if no Benue match
        match_taraba = df_population_taraba[df_population_taraba["Local Government Area"] == lga_name]
        if not match_taraba.empty:
            population = int(match_taraba["Total Population"].values[0])
            age_0_14 = int(match_taraba["0–14"].values[0])

        # Get operational facility count for this LGA from Taraba dataset
        match_facilities_tar = count_health_centers_per_lga_tar[count_health_centers_per_lga_tar["lga"] == lga_name_upper]
        if not match_facilities_tar.empty:
            count_health_centers = int(match_facilities_tar["operational_facility_count"].values[0])

        match_facilities_benue = count_health_centers_per_lga_benue[count_health_centers_per_lga_benue["lga"] == lga_name_upper]
        if not match_facilities_benue.empty:
            count_health_centers = int(match_facilities_benue["operational_facility_count"].values[0])

        feature["properties"]["population"] = population
        feature["properties"]["population_str"] = "{:,}".format(population)
        feature["properties"]["age_0_14"] = age_0_14
        feature["properties"]["age_0_14_str"] = "{:,}".format(age_0_14) 
        feature["properties"]["facility_count"] = count_health_centers
        feature["properties"]["facility_count_str"] = "{:,}".format(count_health_centers)

        green_intensity = max(0, 255 - int((population / max_population) * 255))
        feature["properties"]["color"] = [255, green_intensity, 100, 160]

    else:
        feature["properties"]["population"] = 0
        feature["properties"]["age_0_14"] = 0
        feature["properties"]["facility_count"] = 0
        feature["properties"]["color"] = [200, 200, 200, 50]

st.write("First LGA feature properties:")
st.json(geojson_data["features"][0]["properties"])

###### MAP ######

geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    data=geojson_data,
    stroked=True,
    filled=True,  # now fill the polygons
    get_fill_color="properties.color",  # now reading your precomputed color    
    get_line_color=[80, 80, 80],
    lineWidthMinPixels=0.6,
    pickable=True,
    auto_highlight=True
)

states_layer = pdk.Layer(
    "GeoJsonLayer",
    data=states_geojson_data,
    stroked=True,
    filled=False,  # transparent fill
    get_line_color=[0, 0, 0, 200],  # black border
    lineWidthMinPixels=2
)

# Create scatterplot layer for Cities
cities_layer = pdk.Layer(
    "ScatterplotLayer",
    data=cities_df,
    get_position='[lon, lat]',
    get_color='color',
    get_radius='radius',
    get_elevation='elevation',
    pickable=True,
    auto_highlight=True
)

# Create text labels for cities
labels_layer = pdk.Layer(
    "TextLayer",
    data=cities_df,
    get_position='[lon, lat]',
    get_text='city',
    get_size=17,
    get_color=[0, 0, 0],
    get_angle=0,
    get_alignment_baseline="'bottom'",
    pickable=False,
)

# Create ScatterplotLayer for the Operational Health Centers in Benue
benue_health_centers_layer = pdk.Layer(
    "ScatterplotLayer",
    data=benue_operational_health_centers,  # <- This should be a Python dict or a URL string
    get_position='[longitude, latitude]',
    stroked=False,
    filled=True,
    get_fill_color="[255, 0, 0,160]",  # Or "color" if your DataFrame has a color column
    get_radius=700,
    pickable=True,
    auto_highlight=True
)

# Create ScatterplotLayer for the Operational Health Centers in Taraba
taraba_health_centers_layer = pdk.Layer(
    "ScatterplotLayer",
    data=taraba_operational_health_centers,  # <- This should be a Python dict or a URL string
    get_position='[longitude, latitude]',
    stroked=False,
    filled=True,
    get_fill_color="[0, 0, 255, 160]",  # Or "color" if your DataFrame has a color column
    get_radius=700,
    pickable=True,
    auto_highlight=True
)

# View settings
initial_view_state = pdk.ViewState(
    latitude=7.8,
    longitude=8.45,
    zoom=6,
    pitch=0
)

# Render the map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=initial_view_state,
    layers=[geojson_layer, benue_health_centers_layer, taraba_health_centers_layer, states_layer, cities_layer, labels_layer],
    # use_container_width=True,
    tooltip = {
    "html": """
        <b>State:</b> {state}<br/>
        <b>LGA:</b> {lga}<br/>
        <b>Nr. of Health Centers:</b> {facility_count_str}<br/>
        <b>Est. Total Population:</b> {population_str}<br/>
        <b>Est. Population 0–14:</b> {age_0_14_str}
    """,
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}
))

# Horizontal rule / divider
st.markdown("---")

###### SHOW IMAGES OF NETWORK COVERAGE ######

st.subheader("🗺️ Mobile Network Coverage")

# Image paths or URLs
big_image = "images/airtel.png"
image_2 = "images/glo.png"
image_3 = "images/mtn.png"

# Display the big image full width
st.image(big_image, caption="Airtel", use_column_width=True)

# Create two columns for the side-by-side images
col1, col2 = st.columns(2)

with col1:
    st.image(image_2, caption="Glo", use_column_width=True)

with col2:
    st.image(image_3, caption="MTN", use_column_width=True)



# Add a horizontal divider
st.markdown("---")

# # Data Sources section
# st.markdown("### Data Sources")
# st.markdown("""
# - **City Coordinates:** [GeoNames.org](http://www.geonames.org/)
# - **Map Data:** [OpenStreetMap](https://www.openstreetmap.org/)
# - **Population Density Data:** [WorldPop Project](https://www.worldpop.org/)
# - **Imagery:** Custom images from local directory
# """)



# Add content to the sidebar
st.sidebar.markdown("### 📖 Data Sources")
st.sidebar.markdown("""
- **City Coordinates:** [GeoNames.org](http://www.geonames.org/)
- **Map Data:** [OpenStreetMap](https://www.openstreetmap.org/)
- **Population Density Data:** [WorldPop Project](https://www.worldpop.org/)
- **Imagery:** Local image directory
""")

###### SHOW DATA ######
# Checkbox to show data samples
# if st.checkbox("Show sample data Population per Local Government Area (LGA)"):
#     st.write(operational_health_centers.head())

if st.sidebar.checkbox("Show sample Operational Health Centers data"):
    st.sidebar.subheader("📍 Benue State")
    st.sidebar.dataframe(df_benue_health_centers.head(5))
    
    st.sidebar.subheader("📍 Taraba State")
    st.sidebar.dataframe(df_taraba_health_centers.head(5))