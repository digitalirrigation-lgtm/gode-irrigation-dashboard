import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Irrigation Intelligence - Gode", layout="wide")

translations = {
    "Somali": {
        "title": "🛰️ Sirdoonka Waraabka Dijitaalka ah - Gode Zone",
        "subtitle": "Warbixinta Maalinlaha ah ee u baahan Biyaha Waraabka.",
        "map_title": "🗺️ Khariidadda Caafimaadka Dalagga (Cagaar=Fiican, Casaan=Biyo La'aan)",
        "et_title": "💧 Warbixinta Maalinlaha ah ee Evapotranspiration (ET)",
        "et_evap": "Biyaha ka baxa ciidda (Evaporation):",
        "et_need": "Biyaha uu dalaggu u baahan yahay maanta:",
        "rec_title": "💡 Talo Soo Jeedin Muhiim ah oo ku saabsan beerashada:",
        "rec_text": "MAANTA: Kulaylku waa sarreeyaa (35°C), ET waa 6.2mm. Fur nidaamka waraabka waraabi beeraha subaxdii hore ama makhribkii si looga fogaado uumi-bax sare! Ha beeran bisha Luulyo sababtoo ah roob ma jiro.",
        "legend_healthy": "Aagga Cagaaran: Dalag caafimaad qaba (Biyo ku filan)",
        "legend_dry": "Aagga Cas: Dalag dhibaataysan (Wuxuu u baahan yahay Waraab Degdeg ah)",
        "weather_title": "📊 Qorshaha Cimilada Sanadlaha ah (Luulyo 2026 - Luulyo 2027)",
        "rain_legend": "Casaan = Roob La'aan | Cagaar = Roob Leh | Jaalle = Roob Yar",
        "chart_title": "Heerka Roobka ee Gode Zone ee Satellit-ka ka timid",
        "soil_title": "🟫 Nooca Ciidda (FAO)",
        "soil_info": "Xogta FAO: Ciidda Gode waa ciid carlo-ciid ah oo u baahan waraab sax ah."
    },
    "Amharic": {
        "title": "🛰️ የዲጂታል መስኖ መረጃ ማዕከል - ጎዴ ዞን",
        "subtitle": "ዕለታዊ የሰብል ውሃ ፍላጎት መከታተያ ሪፖርት::",
        "map_title": "🗺️ የሰብል ጤንነት ካርታ (አረንጓዴ=ጥሩ፣ ቀይ=ውሃ የለም/የደረቀ)",
        "et_title": "💧 ዕለታዊ የውሃ ትነት መጠን (Evapotranspiration) ሪፖርት",
        "et_evap": "ከአፈር የሚነን የውሃ መጠን (Evaporation):",
        "et_need": "ሰብሉ ዛሬ የሚፈልገው የውሃ መጠን (Crop Water Need):",
        "rec_title": "💡 ለአርሶ አደሩ ጠቃሚ ምክር፡",
        "rec_text": "ዛሬ፡ የአየር ሙቀቱ ከፍተኛ ነው (35°C)፣ የውሃ ትነት መጠን 6.2mm ነው:: ከፍተኛ ትነትን ለማስወገድ እርሻዎን በማለዳ ወይም በማምሻው ሰዓት ያጠጡ! በሐምሌ ወር ዝናብ ስለሌለ አይዘሩ::",
        "legend_healthy": "አረንጓዴ ዞን: ጤናማ ሰብል (በቂ ...)",
        "legend_dry": "ቀይ ዞን: የተጎዳ ሰብል (አስቸኳይ መስኖ ያስፈልገዋል)",
        "weather_title": "📊 ዓመታዊ የአየር ንብረት እቅድ (ከሐምሌ 2026 እስከ ሐምሌ 2027)",
        "rain_legend": "ቀይ = ዝናብ የለም | አረንጓዴ = ዝናብ አለ | ቢጫ = አነስተኛ ዝናብ",
        "chart_title": "የጎዴ ዞን የዝናብ መጠን ከሳተላይት መረጃ (ሂስቶግራም)",
        "soil_title": "🟫 የአፈር አይነት (FAO)",
        "soil_info": "የFAO መረጃ፡ የጎዴ ዞን አፈር አሸዋማ የሸክላ አፈር (Clay Loam) በመሆኑ ጥንቃቄ የተሞላበት መስኖ ይፈልጋል።"
    },
    "Oromo": {
        "title": "🛰️ Riimootii Jalqaba Masnoo Diijitalii - Gode",
        "subtitle": "Gabaasa Fedhii Bishaan Midhaanii Kan Guyyaa.",
        "map_title": "🗺️ Kaartaa Fayyaa Midhaanii (Magariisa=Gaarii, Diimaa=Bishaan Hin Qabu)",
        "et_title": "💧 Gabaasa Guyyaa Gar-malee Gubachuu Bishaanii (ET)",
        "et_evap": "Bishaan dachee irraa gubatu (Evaporation):",
        "et_need": "Midhaan bishaan guyyaatti barbaadu:",
        "rec_title": "💡 Gorsa Oofishala Meeshaa Masnoo:",
        "rec_text": "GUYYAA HAR'AA: Ho'i jabaadha (35°C), ET n 6.2mm dha. Gubachuu bishaan irraa fagaachuuf ganama ykn galgala masnoo furi! Adoolessa keessa roobni waan hin jirreef hin facasinaa.",
        "legend_healthy": "Iddoo Magariisa: Midhaan gaarii (Bishaan gahaa qaba)",
        "legend_dry": "Iddoo Diimaa: Midhaan miidhame (Masnoo ariifachiisaa barbaada)",
        "weather_title": "📊 Karoora Cimilada Waggaa (Adoolessa 2026 - Adoolessa 2027)",
        "rain_legend": "Diimaa = Rooba Hin Qabu | Magariisa = Rooba Qaba | Keelloo = Rooba Xiqqaa",
        "chart_title": "Agarsiisa Roobaa Godee Satalaayitii Irraa (Histogram)",
        "soil_title": "🟫 Akaakuu Eelee/Achee (FAO)",
        "soil_info": "Ragaa FAO: Cirracha fi dhoqqee kan wal-maku waan ta'eef bishaan sirriitti eeggachuu barbaada."
    },
    "English": {
        "title": "🛰️ Digital Irrigation Intelligence - Gode Zone",
        "subtitle": "Daily Precision Evapotranspiration & Crop Water Needs Metrics.",
        "map_title": "🗺️ Interactive Crop Health Layer Map (Green=Healthy, Red=Water Stress)",
        "et_title": "💧 Daily Evapotranspiration (ET) Metrics Report",
        "et_evap": "Soil Evaporation Level Today:",
        "et_need": "Net Crop Irrigation Requirement:",
        "rec_title": "💡 Precision Agriculture Recommendations:",
        "rec_text": "TODAY: High atmospheric demand (35°C), daily ET is 6.2mm. Trigger drip lines during early morning or late evening hours to maximize Water Use Efficiency (WUE). Reminder: Do not plant new crops in July due to dry spells.",
        "legend_healthy": "Green Zone: Fully turgid, high NDVI vegetation (Optimal moisture status)",
        "legend_dry": "Red Zone: Severe moisture deficit, low NDVI (Immediate irrigation required)",
        "weather_title": "📊 Annual Climate Planning (July 2026 - July 2027)",
        "rain_legend": "Red = No Rain | Green = Wet Season | Yellow = Light Showers",
        "chart_title": "Gode Zone Satellite Climate Precipitation Histogram",
        "soil_title": "🟫 FAO Soil Type Information",
        "soil_info": "FAO Dataset: Gode soil consists mainly of Fluvisols (Clay Loam) requiring controlled drip systems."
    }
}

selected_lang = st.sidebar.selectbox("🌐 Choose Language / Dooro Luqadda / ቋንቋ ይምረጡ", ["Somali", "Amharic", "Oromo", "English"])
text = translations[selected_lang]

st.title(text["title"])
st.write(f"### {text['subtitle']}")

# 1. EVAPOTRANSPIRATION (ET) REPORT METRICS SIDE-BY-SIDE
st.markdown(f"### {text['et_title']}")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label=text["et_evap"], value="2.4 mm / day", delta="High Evaporation", delta_color="inverse")
with m_col2:
    st.metric(label=text["et_need"], value="3.8 mm / day", delta="Total Requirement")
with m_col3:
    st.metric(label="📊 Total Combined Daily ET:", value="6.2 mm", delta="Action Required", delta_color="inverse")

# 2. CLEAR MAP AND CORRESPONDING COLOR CODES
st.markdown(f"### {text['map_title']}")

gode_lat, gode_lon = 5.95, 43.55
gode_map = folium.Map(location=[gode_lat, gode_lon], zoom_start=13, tiles="OpenStreetMap")

folium.Circle([5.952, 43.552], radius=400, color="#2ecc71", fill=True, fill_color="#2ecc71", popup="Healthy Plot").add_to(gode_map)
folium.Circle([5.945, 43.561], radius=350, color="#e74c3c", fill=True, fill_color="#e74c3c", popup="Water Deficit Plot").add_to(gode_map)
folium.Circle([5.958, 43.543], radius=500, color="#2ecc71", fill=True, fill_color="#2ecc71", popup="Healthy Plot").add_to(gode_map)
folium.Circle([5.939, 43.549], radius=300, color="#e74c3c", fill=True, fill_color="#e74c3c", popup="Dry Zone").add_to(gode_map)

st_folium(gode_map, width=1100, height=450, key="gode_crop_health_map")

c1, c2 = st.columns(2)
with c1:
    st.success(text["legend_healthy"])
with c2:
    st.error(text["legend_dry"])

# 3. YEARLY CLIMATE PRECIPITATION HISTOGRAM & FAO SOIL TYPE 
col1, col2 = st.columns(2)
with col1:
    st.subheader(text["weather_title"])
    st.info(text["rain_legend"])
    
    fig, ax = plt.subplots(figsize=(6, 3))
    # Planning Horizon: July 2026 through July 2027
    months = ['Jul26', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan27', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul27']
    rainfall_levels = [0, 5, 0, 65, 80, 20, 10, 15, 40, 95, 50, 5, 0]
    
    colors = ['#e74c3c' if r < 15 else '#f1c40f' if r < 45 else '#2ecc71' for r in rainfall_levels]
    ax.bar(months, rainfall_levels, color=colors, edgecolor='black')
    ax.set_title(text["chart_title"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader(text["soil_title"])
    st.success(text["soil_info"])
    st.markdown("### 🗺️ Visual Soil Grid Map")
    st.markdown("| 🟧 Clay Area | 🟨 Sand Area |\n|---|---|\n| 🟩 River Basin | 🟧 Clay Area Vin |")

st.markdown("---")
st.error(f"### {text['rec_title']}\n{text['rec_text']}")
