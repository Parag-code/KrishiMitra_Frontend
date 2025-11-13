import streamlit as st
import requests
import json
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE")
KRISHIMITRA_API_KEY = os.getenv("KRISHIMITRA_API_KEY")
HEADERS = {"x-api-key": KRISHIMITRA_API_KEY}

import time

def typewriter(text, speed=0.01):
    box = st.empty()
    out = ""

    for ch in text:
        out += ch
        box.markdown(
            f"<div class='result-box'>{out}<span class='typing-cursor'></span></div>",
            unsafe_allow_html=True
        )
        time.sleep(speed)

    box.markdown(
        f"<div class='result-box'>{out}</div>",
        unsafe_allow_html=True
    )


def show_loader(message="Processing..."):
    loader_area = st.empty()
    loader_area.markdown(f"""
    <div style='text-align:center; margin-top:15px;'>
        <div class='custom-loader'></div>
        <div class='loader-text'>{message}</div>
    </div>
    """, unsafe_allow_html=True)
    return loader_area


st.set_page_config(page_title="KrishiMitra", page_icon="🌾", layout="wide")


st.sidebar.image("KrishiMitra_logo.png", width=130)


st.sidebar.markdown("""
<div class="sidebar-title-box">
    <h1>KrishiMitra</h1>
    <p>India’s Smart Kheti Assistant 🤖</p>
</div>
""", unsafe_allow_html=True)

section = st.sidebar.radio(
    "Select Service",
    [
        "💬 Ask KrishiMitra",
        "🌾 Crop Recommendation",
        "🧪 Soil & Fertilizer Advice",
        "💧 Irrigation Guidance",
        "🍃 Disease Detection"
    ]
)

st.markdown("""
<style>
/* ===== PropertyPulse Dark Navy Blue Theme (Final Polished Version) ===== */

/* Remove Streamlit top header and extend gradient */
[data-testid="stHeader"] {
  background: transparent !important;
  height: 0rem !important;
  visibility: hidden;
}

/* Main App Background */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #0b1320 0%, #060910 100%) !important;
  color: #f2f6fc !important;
  font-family: 'Poppins', sans-serif;
  padding-top: 0 !important;
  margin-top: 0 !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #131b27 0%, #0b1018 100%) !important;
  color: #e5e9f0 !important;
  border-right: 1px solid #1c2532;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
  color: #e5e9f0 !important;
}

/* Headings */
h1, h2, h3, h4 {
  color: #e2e8f9 !important;
  font-weight: 700;
  font-family: 'Poppins', sans-serif;
}

/* Buttons */
.stButton button {
  background: linear-gradient(90deg, #007bff, #0044cc);
  color: #ffffff !important;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  padding: 0.6em 1.3em;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.25);
  transition: all 0.3s ease;
}
.stButton button:hover {
  transform: scale(1.04);
  background: linear-gradient(90deg, #0056d2, #007bff);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
}

/* Inputs */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
  background-color: #141c29 !important;
  color: #eaf2ff !important;
  border: 1px solid #2b3850 !important;
  border-radius: 8px;
  font-weight: 500;
  padding: 0.4em 0.6em;
  transition: border-color 0.3s ease;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: #007bff !important;
  box-shadow: 0 0 6px #007bff;
}

/* Result Box */
.result-box {
  background: linear-gradient(145deg, #141c2c, #0e1522);
  border-left: 5px solid #1e88e5;
  box-shadow: 0 0 12px rgba(30, 136, 229, 0.25);
  color: #d7e7ff;
  padding: 15px 20px;
  border-radius: 10px;
  margin-top: 12px;
  margin-bottom: 8px;
  line-height: 1.6;
  font-size: 16px;
}

/* Ultra-light faded mint green success box */
div[role="alert"] {
    background: rgba(0, 255, 150, 0.10) !important;   /* very light mint */
    border-left: 5px solid rgba(0, 255, 150, 0.25) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 15px rgba(0, 255, 150, 0.08) !important;
    padding: 12px 15px !important;
}

div[role="alert"] p {
    color: #eafff4 !important;   /* mint white-green */
    font-weight: 500;
}


.stError {
  background: linear-gradient(90deg, #661818, #9b1c1c) !important;
  color: #fff !important;
  border-radius: 8px;
}
.stWarning {
  background: linear-gradient(90deg, #664d00, #a67c00) !important;
  color: #fff !important;
  border-radius: 8px;
}

/* Compact Layout */
section[data-testid="stVerticalBlock"] {
  padding: 0 !important;
  margin: 0 !important;
}
[data-testid="stMarkdownContainer"] {
  margin: 0.4rem 0 !important;
}
.block-container {
  padding-top: 0 !important;
}

/* SelectBox Styling — same as input fields */
div[data-baseweb="select"] > div {
    background-color: #141c29 !important;
    border: 1px solid #2b3850 !important;
    border-radius: 8px !important;
    color: #eaf2ff !important;
    padding: 4px 6px !important;
}

/* Arrow icon color */
div[data-baseweb="select"] svg {
    fill: #eaf2ff !important;
}

/* Hover effect */
div[data-baseweb="select"]:hover > div {
    border-color: #3b4a6a !important;
}

/* Focus / menu open */
div[data-baseweb="select"][aria-expanded="true"] > div {
    border-color: #007bff !important;
    box-shadow: 0 0 6px #007bff !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background-color: #141c29 !important;
    border: 1px solid #2b3850 !important;
    border-radius: 8px !important;
}

/* Dropdown options */
ul[role="listbox"] li {
    color: #eaf2ff !important;
    padding: 8px 10px !important;
}

/* Hover option */
ul[role="listbox"] li:hover {
    background-color: #1c2738 !important;
}
/* FIX: Selectbox text clipping in latest Streamlit */
div[data-baseweb="select"] span {
    line-height: 1.8 !important;
    padding-top: 6px !important;
    padding-bottom: 6px !important;
    display: flex !important;
    align-items: center !important;
    overflow: visible !important;
}

/* Increase height of the whole select container */
div[data-baseweb="select"] {
    min-height: 48px !important;
}

/* Extra safety: avoid cutting inside children */
div[data-baseweb="select"] * {
    overflow: visible !important;
}

/* Sidebar title premium box */
.sidebar-title-box {
    background: linear-gradient(145deg, #162235, #0f1724);
    border: 1px solid #1e2d42;
    padding: 18px 16px;
    border-radius: 12px;
    margin-bottom: 20px;
    text-align: left;
    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
}

.sidebar-title-box h1 {
    font-size: 26px;
    color: #e2e8f9 !important;
    margin-bottom: 6px;
}

.sidebar-title-box p {
    color: #b7c4d8 !important;
    font-size: 14px;
    margin: 0;
}

/* Main Title Box (PropertyPulse style) */
.main-title-box {
    background: linear-gradient(145deg, #0d1a2e, #0a1421);
    border: 1px solid #1e3a5f;
    padding: 22px 28px;
    border-radius: 14px;
    margin-bottom: 25px;
    margin-top: -10px;
    box-shadow: 0 4px 14px rgba(1, 45, 90, 0.35);
}

.main-title-box h1 {
    margin: 0;
    padding: 0;
    font-size: 32px;
    color: #e2e8f9 !important;
    font-weight: 700;
}

/* Custom Glowing Loader */
.custom-loader {
  border: 4px solid rgba(0, 255, 150, 0.15);
  border-top: 4px solid #00ff99;
  border-radius: 50%;
  width: 42px;
  height: 42px;
  animation: spinner 1s linear infinite, glowPulse 1.5s ease-in-out infinite alternate;
  margin: 10px auto;
}

@keyframes spinner {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes glowPulse {
  0% { box-shadow: 0 0 8px #00ff99; }
  100% { box-shadow: 0 0 20px #00ffcc; }
}

.loader-text {
  color: #c1ffe9;
  font-size: 15px;
  text-align: center;
  margin-top: 6px;
}



</style>

""", unsafe_allow_html=True)

st.markdown("""
<style>
.typing-cursor {
  display: inline-block;
  width: 8px;
  background: #00ff99;
  margin-left: 3px;
  animation: blink 0.7s steps(1) infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)


if section == "💬 Ask KrishiMitra":
    st.markdown("""
<div class="main-title-box">
    <h1>💬 Ask KrishiMitra Anything!</h1>
</div>
""", unsafe_allow_html=True)
    query = st.text_area("Query:", placeholder="Example: Gehu me paani kitni baar dena chahiye?")
    if st.button("Get Answer"):
        if query.strip():
            loader = show_loader("KrishiMitra soch raha hai...")
            res = requests.post(
            API_BASE,
            json={"query": query},
            headers={
        "x-api-key": KRISHIMITRA_API_KEY,
        "Content-Type": "application/json"
    }
    )

            loader.empty()
            if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Answer Ready!")
                    typewriter(data.get("answer", ""))
            else:
                    st.error("⚠️ Backend error. Please check your Flask API.")
        else:
            st.warning("Please enter your question first!")

elif section == "🌾 Crop Recommendation":
    st.markdown("""
<div class="main-title-box">
    <h1>🌾 Get Best Crop Suggestions</h1>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("📍 Location", "Jaipur")
    with col2:
        season = st.selectbox("🗓️ Season", ["Kharif", "Rabi", "Zaid"])
    if st.button("Recommend Crops"):
        payload = {"location": location, "season": season}
        loader = show_loader("Analyzing live weather & soil...")
        res = requests.post(
        API_BASE,
        json=payload,
        headers={
            "x-api-key": KRISHIMITRA_API_KEY,
            "Content-Type": "application/json"
        }
    )
        loader.empty()

        if res.ok:
                data = res.json()["result"]
                crops = data.get("crops", [])
                summary = data.get("summary", "")
                st.success("✅ Crop Recommendation Ready!")
                for crop in crops:
                    st.markdown(f"<h4>🌿 <b>{crop['name']}</b> ({crop['type']})</h4>", unsafe_allow_html=True)
                    typewriter(f"🧠 Reason: {crop['reason']}")
                    typewriter(f"🔄 Rotation Tip: {crop['rotation_tip']}")
                typewriter(f"🧾 Summary:\n{summary}")
        else:
                st.error("❌ Failed to get response. Check Flask logs.")

elif section == "🧪 Soil & Fertilizer Advice":
    st.markdown("""
<div class="main-title-box">
    <h1>🧪 Soil & Fertilizer Analysis</h1>
</div>
""", unsafe_allow_html=True)

    crop = st.text_input("🌾 Crop", "Wheat")
    location = st.text_input("📍 Location", "Lucknow")
    if st.button("Analyze Soil"):
        payload = {"crop": crop, "location": location}
        loader = show_loader("Fetching soil & weather data...")
        res = requests.post(
        API_BASE,
        json=payload,
        headers={
            "x-api-key": KRISHIMITRA_API_KEY,
            "Content-Type": "application/json"
        }
    )

        loader.empty()

        if res.ok:
                data = res.json()["result"]
                st.success("✅ Soil Analysis Ready!")
                text = (
    f"🧪 Recommended Fertilizer: {data.get('fertilizer')}\n\n"
    f"⚖️ Dose & Method: {data.get('dose_hint')}\n\n"
    f"🌿 Explanation: {data.get('explanation')}"
)
                typewriter(text)

        else:
                st.error("⚠️ Backend error. Check Flask server.")

elif section == "💧 Irrigation Guidance":
    st.markdown("""
<div class="main-title-box">
    <h1>💧 Smart Irrigation Plan</h1>
</div>
""", unsafe_allow_html=True)

    city = st.text_input("📍 City", "Delhi")
    crop = st.text_input("🌾 Crop", "Rice")
    soil_type = st.selectbox("🌱 Soil Type", ["Loamy", "Clayey", "Sandy", "Black"])
    if st.button("Get Irrigation Tips"):
        payload = {"city": city, "crop": crop, "soil_type": soil_type}
        loader = show_loader("Predicting irrigation pattern...")
        res = requests.post(
        API_BASE,
        json=payload,
        headers={
            "x-api-key": KRISHIMITRA_API_KEY,
            "Content-Type": "application/json"
        }
    )
        loader.empty()

        if res.ok:
                data = res.json()["result"]
                st.success("✅ Irrigation Advice Ready!")
                typewriter(f"🌦️ Weather Trend:\n{data.get('weather_trend')}")
                typewriter(f"💧 Advice:\n{data.get('irrigation_advice')}")

        else:
                st.error("❌ Flask API did not respond properly.")

elif section == "🍃 Disease Detection":
    st.markdown("""
<div class="main-title-box">
    <h1>🍃 Leaf Disease Detection</h1>
</div>
""", unsafe_allow_html=True)

    file = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"])
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(file.read())
            tmp.flush()
        try:
            with open(tmp.name, "rb") as f:
                files = {"file": f}
                loader_area = st.empty()
                loader_area.markdown("""
<div style='text-align:center; margin-top:15px;'>
    <div class='custom-loader'></div>
    <div class='loader-text'>Analyzing leaf image...</div>
</div>
""", unsafe_allow_html=True)
                res = requests.post(
                API_BASE,
                files=files,
                headers={"x-api-key": KRISHIMITRA_API_KEY}
            ) 

                loader_area.empty()
        finally:
            try:
                os.remove(tmp.name)
            except PermissionError:
                pass

        if res.ok:
            data = res.json()["result"]
            st.success("✅ Analysis Complete!")
            st.image(file, caption="Uploaded Leaf", width=350)

            st.markdown(f"### 🦠 Disease: **{data['disease']}**")
            typewriter(data.get("summary",""))

            if data.get("remedy"):
                st.markdown("#### 🌿 Suggested Remedies:")
                for line in data["remedy"]:
                    clean_line = (
                        line.replace("Line 1:", "")
                            .replace("Line 2:", "")
                            .replace("Line 3:", "")
                            .replace("Line:", "")
                            .strip()
                    )
                    typewriter("• " + clean_line)

        else:
            st.error("⚠️ Failed to analyze image. Check Flask logs.")
