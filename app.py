import streamlit as st
import json
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="UP Sahayata | Private Info Portal", page_icon="🇮🇳", layout="centered")

# --- 2. LANGUAGE DICTIONARY ---
texts = {
    "English": {
        "disclaimer_title": "⚠️ Legal Disclaimer",
        "disclaimer_body": "This is a **Private Information Portal**. We are NOT affiliated with the Government of Uttar Pradesh or India. All data is for informational purposes only. Please verify with [UP.gov.in](https://up.gov.in) before applying.",
        "footer_text": "Private Portal | Not Government Official | DPDP Act 2025 Compliant",
        "age_label": "Enter Age",
        "income_label": "Annual Income (₹)",
        "button": "SEARCH SCHEMES"
    },
    "Hindi": {
        "disclaimer_title": "⚠️ कानूनी अस्वीकरण",
        "disclaimer_body": "यह एक **निजी सूचना पोर्टल** है। हम उत्तर प्रदेश या भारत सरकार से संबद्ध नहीं हैं। सभी डेटा केवल सूचनात्मक उद्देश्यों के लिए है। आवेदन करने से पहले [UP.gov.in](https://up.gov.in) से सत्यापित करें।",
        "footer_text": "निजी पोर्टल | सरकारी आधिकारिक नहीं | DPDP एक्ट 2025 के अनुरूप",
        "age_label": "उम्र दर्ज करें",
        "income_label": "वार्षिक आय (₹)",
        "button": "योजनाएं खोजें"
    }
}

lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
t = texts[lang]

# --- 3. MANDATORY DISCLAIMER BOX ---
st.warning(f"**{t['disclaimer_title']}**: {t['disclaimer_body']}")

# --- 4. INPUT FORM ---
with st.form("input_form"):
    st.subheader("Check Eligibility")
    age = st.number_input(t["age_label"], 0, 100, 25)
    income = st.number_input(t["income_label"], 0, 1000000, 50000)
    submitted = st.form_submit_button(t["button"], use_container_width=True)

# --- 5. UPDATED LEGAL FOOTER ---
st.markdown(f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333333;
        color: #cccccc;
        text-align: center;
        padding: 5px;
        font-size: 12px;
    }}
    </style>
    <div class="footer">
        {t['footer_text']} | Last Updated: {datetime.now().strftime('%d %b %Y')}
    </div>
    """, unsafe_allow_html=True)
