import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Irrigation Intelligence - Gode", layout="wide")

translations = {
    "Somali": {
        "title": "🛰️ Sirdoonka Waraabka Dijitaalka ah - Gode Zone",
        "subtitle": "Ka fiiri beerkaaga meel kasta oo aad ku raaxaysato adoo adeegsanaya dayax-gacmeedka.",
        "weather_title": "📊 Sifooyinka Cimilada Sanadlaha ah & Toddobaadlaha ah",
        "soil_title": "🟫 Nooca Ciidda (FAO)",
        "soil_info": "Xogta FAO: Ciidda Gode waa ciid carlo-ciid ah oo u baahan waraab sax ah.",
        "rec_title": "💡 Talo Soo Jeedin Muhiim ah oo ku saabsan beerashada:",
        "rec_text": "DIGNIIN: Ha beeran bisha Luulyo ama Sebtembar sababtoo her roob ma jiro. Adeegso biyaha waraabka Wabiga Shabelle si dalaggu u badbaado!",
        "rain_legend": "Casaan = Roob La'aan | Cagaar = Roob Leh | Jaalle = Roob Yar",
        "chart_title": "Heerka Roobka ee Gode Zone (Histogram)"
    },
    "Amharic": {
        "title": "🛰️ የዲጂታል መስኖ መረጃ ማዕከል - ጎዴ ዞን",
        "subtitle": "እርሻዎን ባሉበት ምቹ ቦታ ሆነው በሳተላይት ምስል በቀጥታ ይከታተሉ::",
        "weather_title": "📊 ዓመታዊ እና ሳምንታዊ የአየር ንብረት ሁኔታ",
        "soil_title": "🟫 የአፈር አይነት (FAO)",
        "soil_info": "የFAO መረጃ፡ የጎዴ ዞን አፈር አሸዋማ የሸክላ አፈር (Clay Loam) በመሆኑ ጥንቃቄ የተሞላበት መስኖ ይፈልጋል።",
        "rec_title": "💡 ለአርሶ አደሩ ጠቃሚ ምክር፡",
        "rec_text": "ማስጠንቀቂያ፡ በሐምሌ ወይም በመስከረም ወር ዝናብ ስለሌለ በምንም መንገድ እንዳይዘሩ! በምትኩ የዋቢ ሸበሌ ወንዝ የመስኖ ውሃ ይጠቀሙ።",
        "rain_legend": "ቀይ = ዝናብ የለም | አረንጓዴ = ዝናብ አለ | ቢጫ = አነስተኛ ዝናብ",
        "chart_title": "የጎዴ ዞን የዝናብ መጠን ስርጭት (ሂስቶግራም)"
    },
    "Oromo": {
        "title": "🛰️ Riimootii Jalqaba Masnoo Diijitalii - Gode",
        "subtitle": "Iddoo teessan irraa satalaayitiidhaan lafa keessan live hordofaa.",
        "weather_title": "📊 Haala Qilleensaa Waggaa fi Torbananii",
        "soil_title": "🟫 Akaakuu Eelee/Achee (FAO)",
        "soil_info": "Ragaa FAO: Cirracha fi dhoqqee kan wal-maku waan ta'eef bishaan sirriitti eeggachuu barbaada.",
        "rec_title": "💡 Gorsa Oofishala Meeshaa Masnoo:",
        "rec_text": "Akeekkachiisa: Adoolessa fi Fulbaana keessa roobni waan hin jirreef hin facasinaa! Bishaan masnoo fayyadamaa.",
        "rain_legend": "Diimaa = Rooba Hin Qabu | Magariisa = Rooba Qaba | Keelloo = Rooba Xiqqaa",
        "chart_title": "Agarsiisa Roobaa Godee (Histogram)"
    },
    "English": {
        "title": "🛰️ Digital Irrigation Intelligence - Gode Zone",
        "subtitle": "Watch your farm live from your comfortable place via extreme satellite visualizer.",
        "weather_title": "📊 Annual Climate & Weekly Weather Metrics",
        "soil_title": "🟫 FAO Soil Type Information",
        "soil_info": "FAO Dataset: Gode soil consists mainly of Fluvisols (Clay Loam) requiring controlled drip systems.",
        "rec_title": "💡 Precision Agriculture Recommendations:",
        "rec_text": "CRITICAL WARNING: Do not plant crops in July or September due to extreme dry spells. Rely entirely on Shabelle River irrigation channels to save your investment.",
        "rain_legend": "Red = No Rain | Green = Wet Season | Yellow = Light Showers",
        "chart_title": "Gode Zone Climate Precipitation Histogram"
    }
}

selected_lang = st.sidebar.selectbox("🌐 Choose Language", ["Somali", "Amharic", "Oromo", "English"])
text = translations[selected_lang]

st.title(text["title"])
st.write(f"### {text['subtitle']}")

# INSTANT LOADING MAP CONFIGURATION
gode_lat, gode_lon = 5.95, 43.55

# We use the 'Esri Satellite' map stream which loads instantly without server lag!
gode_map = folium.Map(
    location=[gode_lat, gode_lon], 
    zoom_start=12,
    tiles='https://arcgisonline.com{z}/{y}/{x}',
    attr='Esri Satellite Imagery'
)

# Add a marker over the Shabelle River irrigation zone
folium.Marker(
    [gode_lat, gode_lon], 
    popup="Gode Agriculture Center", 
    icon=folium.Icon(color="green", icon="leaf")
).add_to(gode_map)

# Render map instantly
st_folium(gode_map, width=1100, height=500, key="gode_map_instance")

col1, col2 = st.columns(2)
with col1:
    st.subheader(text["weather_title"])
    st.info(text["rain_legend"])
    fig, ax = plt.subplots(figsize=(6, 3))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    rainfall_levels = [10, 15, 40, 95, 50, 5, 0, 5, 0, 65, 80, 20]
    
    colors = ['#e74c3c' if r < 15 else '#f1c40f' if r < 45 else '#2ecc71' for r in rainfall_levels]
    ax.bar(months, rainfall_levels, color=colors, edgecolor='black')
    ax.set_title(text["chart_title"])
    st.pyplot(fig)

with col2:
    st.subheader(text["soil_title"])
    st.success(text["soil_info"])
    st.markdown("### 🗺️ Visual Soil Grid Map")
    st.markdown("| 🟧 Clay Area | 🟨 Sand Area |\n|---|---|\n| 🟩 River Basin | 🟧 Clay Area Vin |")

st.markdown("---")
st.error(f"### {text['rec_title']}\n{text['rec_text']}")
