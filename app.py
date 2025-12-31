import streamlit as st
import json
import requests
from datetime import datetime

# --- 1. CONFIG & DATA ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="wide")

# Get today's date for the footer
current_date = datetime.now().strftime("%d %B %Y")

# --- 2. CUSTOM CSS FOR CARDS & FOOTER ---
st.markdown(f"""
    <style>
    .main {{
        background-color: #f0f2f6;
    }}
    .scheme-card {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        border-left: 8px solid #ff9933; /* Saffron border */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }}
    .benefit-text {{
        color: #1e7e34;
        font-weight: 700;
        font-size: 1.15em;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #003366;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
        z-index: 100;
    }}
    </style>
    <div class="footer">
        🚀 Updated for 2026 | Last Sync: {current_date} | Government of Uttar Pradesh Data 🇮🇳
    </div>
    """, unsafe_allow_html=True)

# (Previous load_data function remains the same)
def load_data():
    try:
        with open('schemes.json', 'r') as f:
            return json.load(f)
    except:
        return []

# --- 3. APP CONTENT ---
st.title("🇮🇳 UP Sahayata: Scheme Finder 2026")
st.caption("Helping Agra & UP citizens find the right government support instantly.")

# (Input logic remains same as previous version)
age = st.sidebar.number_input("Enter Age", 0, 110, 25)
income = st.sidebar.number_input("Annual Income (₹)", 0, 2000000, 50000)

if st.sidebar.button("Find Schemes", type="primary"):
    schemes = load_data()
    found = False
    for s in schemes:
        if age >= s['min_age'] and income <= s['max_income']:
            found = True
            with st.container():
                st.markdown(f"""
                <div class="scheme-card">
                    <h2 style='color:#003366; margin-top:0;'>{s['name']}</h2>
                    <p class="benefit-text">🎁 Benefit: {s['benefit']}</p>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Required Documents / दस्तावेज"):
                    # Use the Raw GitHub links you found
                    cols = st.columns(len(s['docs']))
                    for i, doc in enumerate(s['docs']):
                        img = s['doc_images'].get(doc, "https://img.icons8.com/color/144/document.png")
                        cols[i].image(img, width=50, caption=doc)
    if not found:
        st.info("No schemes match currently. Try lower income or different age.")

# Space at bottom so footer doesn't hide content
st.markdown("<br><br><br>", unsafe_allow_html=True)
