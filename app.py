import streamlit as st
import json
import requests
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- 2. LANGUAGE DICTIONARY ---
texts = {
    "English": {
        "title": "🇮🇳 UP Sahayata | Scheme Finder",
        "subtitle": "Enter details to find eligible schemes.",
        "age_label": "Enter Age",
        "income_label": "Annual Income (₹)",
        "button": "SEARCH SCHEMES",
        "results": "Eligible Schemes",
        "no_results": "No schemes found. Try different criteria.",
        "docs": "Required Documents",
        "footer": "Updated: 2026 | UP Government Data"
    },
    "Hindi": {
        "title": "🇮🇳 यूपी सहायता | योजना खोजें",
        "subtitle": "पात्र योजनाओं को खोजने के लिए विवरण दर्ज करें।",
        "age_label": "उम्र दर्ज करें",
        "income_label": "वार्षिक आय (₹)",
        "button": "योजनाएं खोजें",
        "results": "आपके लिए योजनाएं",
        "no_results": "कोई योजना नहीं मिली। कृपया विवरण बदलें।",
        "docs": "जरूरी दस्तावेज",
        "footer": "अपडेटेड: 2026 | उत्तर प्रदेश सरकार डेटा"
    }
}

# Language Selector
lang = st.radio("Select Language / भाषा चुनें", ["English", "Hindi"], horizontal=True)
t = texts[lang]

# --- 3. CUSTOM STYLE ---
st.markdown(f"""
    <style>
    .stNumberInput label {{ font-size: 22px !important; font-weight: bold !important; color: #003366 !important; }}
    .scheme-card {{ background-color: #ffffff; border-radius: 12px; padding: 20px; border-left: 10px solid #ff9933; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; background-color: #003366; color: white; text-align: center; padding: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.title(t["title"])
st.info(t["subtitle"])

with st.form("input_form"):
    age = st.number_input(t["age_label"], min_value=0, max_value=120, value=25)
    income = st.number_input(t["income_label"], min_value=0, value=50000, step=5000)
    submitted = st.form_submit_button(t["button"], use_container_width=True)

# --- 5. RESULTS ---
if submitted:
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            schemes = json.load(f)
    except: schemes = []

    found = False
    st.subheader(t["results"])
    
    for s in schemes:
        if age >= s['min_age'] and income <= s['max_income']:
            found = True
            # Display Title in Hindi if Hindi is selected
            display_name = s['name_hindi'] if lang == "Hindi" else s['name']
            display_benefit = s['benefit_hindi'] if lang == "Hindi" else s['benefit']
            
            st.markdown(f"""
            <div class="scheme-card">
                <h2 style='margin:0; color:#003366;'>{display_name}</h2>
                <p style='color:#1e7e34; font-weight:bold; font-size:1.2em;'>{display_benefit}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(t["docs"]):
                cols = st.columns(3)
                for i, doc in enumerate(s['docs']):
                    img = s['doc_images'].get(doc, "https://img.icons8.com/color/144/document.png")
                    cols[i%3].image(img, width=60, caption=doc)
    
    if not found:
        st.warning(t["no_results"])

st.markdown(f"<div class='footer'>{t['footer']}</div>", unsafe_allow_html=True)
