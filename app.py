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
        "legend_dry": "Aagga Cas: Dalag dhibaataysan (Wuxuu u baahan yahay Waraab Degdeg ah)"
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
        "legend_healthy": "አረንጓዴ ዞን: ጤናማ ሰብል (በቂ ውሃ አለው)",
        "legend_dry": "ቀይ ዞን: የተጎዳ ሰብል (አስቸኳይ መስኖ ያስፈልገዋል)"
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
        "legend_dry": "Iddoo Diimaa: Midhaan miidhame (Masnoo ariifachiisaa barbaada)"
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
        "legend_dry": "Red Zone: Severe moisture deficit, low NDVI (Immediate irrigation required)"
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

# Add a pre-computed spatial map structure representing Gode's Shabelle River farming grid
# Circle markers display exact crop zones clearly without white cloud blurs
folium.Circle([5.952, 43.552], radius=400, color="#2ecc71", fill=True, fill_color="#2ecc71", popup="Healthy Plot").add_to(gode_map)
folium.Circle([5.945, 43.561], radius=350, color="#e74c3c", fill=True, fill_color="#e74c3c", popup="Water Deficit Plot").add_to(gode_map)
folium.Circle([5.958, 43.543], radius=500, color="#2ecc71", fill=True, fill_color="#2ecc71", popup="Healthy Plot").add_to(gode_map)
folium.Circle([5.939, 43.549], radius=300, color="#e74c3c", fill=True, fill_color="#e74c3c", popup="Dry Zone").add_to(gode_map)

# Render the interactive map block cleanly
st_folium(gode_map, width=1100, height=450, key="gode_crop_health_map")

# Visual legend box beneath the layout map canvas
c1, c2 = st.columns(2)
with c1:
    st.success(text["legend_healthy"])
with c2:
    st.error(text["legend_dry"])

# 3. DIRECT ACTION RECOMMENDATIONS FOOTER BOX
st.markdown("---")
st.error(f"### {text['rec_title']}\n{text['rec_text']}")
