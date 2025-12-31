import streamlit as st
import json
import requests
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- 2. CUSTOM STYLE (Focus on Visibility) ---
st.markdown("""
    <style>
    /* Make input labels bigger and bolder */
    .stNumberInput label, .stTextInput label {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #003366 !important;
    }
    /* Style the result cards */
    .scheme-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border-left: 10px solid #ff9933;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #003366;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    try:
        with open('schemes.json', 'r') as f:
            return json.load(f)
    except:
        return []

# --- 3. MAIN INTERFACE ---
st.title("🇮🇳 UP Sahayata | उत्तर प्रदेश सहायता")
st.info("Enter details below to find your eligible schemes.")

# Large, Visible Entry Taker
with st.form("input_form"):
    st.subheader("Personal Details / व्यक्तिगत जानकारी")
    age = st.number_input("Enter Age / अपनी उम्र लिखें", min_value=0, max_value=120, value=25)
    income = st.number_input("Annual Income / वार्षिक आय (₹)", min_value=0, value=50000, step=5000)
    
    submitted = st.form_submit_button("SEARCH SCHEMES / योजनाएं खोजें", use_container_width=True)

# --- 4. RESULTS ---
if submitted:
    schemes = load_data()
    found = False
    
    for s in schemes:
        if age >= s['min_age'] and income <= s['max_income']:
            found = True
            st.markdown(f"""
            <div class="scheme-card">
                <h2 style='margin:0;'>{s['name']}</h2>
                <p style='color:green; font-weight:bold; font-size:1.2em;'>Benefit: {s['benefit']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Required Documents / दस्तावेज देखें"):
                cols = st.columns(3)
                for i, doc in enumerate(s['docs']):
                    img = s['doc_images'].get(doc, "https://img.icons8.com/color/144/document.png")
                    cols[i%3].image(img, width=60, caption=doc)
    
    if not found:
        st.warning("No schemes found. Try a different age or lower income.")

# Footer
st.markdown(f"""
    <div class="footer">
        Updated: {datetime.now().strftime('%d %B %Y')} | Data: UP Government 🇮🇳
    </div>
    """, unsafe_allow_html=True)
