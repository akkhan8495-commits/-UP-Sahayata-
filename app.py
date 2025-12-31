import streamlit as st
import json
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- 2. LANGUAGE DATA ---
texts = {
    "English": {
        "title": "🇮🇳 UP Sahayata | Private Portal",
        "search_btn": "SEARCH SCHEMES",
        "ad_disclaimer": "This link will refer you to Amazon website for buying.",
        "amazon_info": "As an Amazon Associate, I earn from qualifying purchases.",
        "footer": "Private Portal | Not Government Official",
        "show_policy": "Show Privacy Policy & Legal",
        "hide_policy": "Hide Privacy Policy"
    },
    "Hindi": {
        "title": "🇮🇳 यूपी सहायता | निजी सूचना पोर्टल",
        "search_btn": "योजनाएं खोजें",
        "ad_disclaimer": "यह लिंक आपको खरीदारी के लिए अमेज़न वेबसाइट पर ले जाएगा।",
        "amazon_info": "एक अमेज़न एसोसिएट के रूप में, मैं योग्य खरीदारी से कमाता हूँ।",
        "footer": "निजी पोर्टल | सरकारी आधिकारिक नहीं",
        "show_policy": "गोपनीयता नीति और कानूनी जानकारी देखें",
        "hide_policy": "गोपनीयता नीति छिपाएं"
    }
}

# --- 3. LANGUAGE SELECTOR (Top of Page) ---
lang = st.radio("Select Language / भाषा चुनें", ["English", "Hindi"], horizontal=True)
t = texts[lang]

# --- 4. MAIN SCHEME FINDER ---
st.title(t["title"])
st.warning("⚠️ **Disclaimer**: Not a Government App. Verify at up.gov.in.")

with st.form("input_form"):
    age = st.number_input("Age", 0, 100, 25)
    income = st.number_input("Income (₹)", 0, 1000000, 50000)
    submitted = st.form_submit_button(t["search_btn"], use_container_width=True)

if submitted:
    # Logic to load and show schemes...
    st.success("Showing eligible schemes below:")
    # (Affiliate Link Example)
    st.link_button("📁 Buy Document Folder", "https://topdeal.in/your-link")
    st.caption(t["ad_disclaimer"])
    st.info(t["amazon_info"])

# --- 5. BOTTOM PRIVACY TOGGLE ---
st.markdown("---")
if "show_legal" not in st.session_state:
    st.session_state.show_legal = False

if st.button(t["hide_policy"] if st.session_state.show_legal else t["show_policy"]):
    st.session_state.show_legal = not st.session_state.show_legal

if st.session_state.show_legal:
    st.markdown(f"""
    ### Privacy Policy & Legal (DPDP Act 2025)
    - **No Storage**: We do not store your age/income.
    - **Affiliate**: We use EarnKaro & Amazon tracking cookies.
    - **Amazon**: As an Amazon Associate, I earn from qualifying purchases.
    - **Contact**: akkhan8495@gmail.com
    *Updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 6. SIMPLE FOOTER ---
st.markdown(f"<p style='text-align:center; color:gray; font-size:10px;'>{t['footer']} | 2026</p>", unsafe_allow_html=True)

