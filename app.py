import streamlit as st
import json
from datetime import datetime

# --- 1. SETTINGS & SECURITY SHIELD ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# This CSS hides the 'GitHub' and 'Manage App' buttons from your users
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# --- 2. SECURE DATA LOADING ---
def get_data():
    try:
        # Pulls data from the 'Secrets' tab (NOT a visible file)
        # Format in Secrets should be: SCHEME_DATA = ''' [your json] '''
        return json.loads(st.secrets["SCHEME_DATA"])
    except Exception:
        st.error("Secure data connection failed. Ensure Secrets are configured.")
        return []

# --- 3. STABLE TABS ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)

    with st.form("main_search"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submitted = st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True)

    if submitted:
        schemes = get_data()
        found_any = False
        
        # Iterates through every scheme in your secret data
        for i, s in enumerate(schemes):
            if age >= s['min_age'] and income <= s['max_income']:
                found_any = True
                name = s.get('name_hindi' if lang == "Hindi" else 'name', s['name'])
                benefit = s.get('benefit_hindi' if lang == "Hindi" else 'benefit', s['benefit'])
                
                # Professional Result Card
                st.success(f"### {name}")
                st.write(f"**Benefit:** {benefit}")
                
                # Unique labels prevent 'Duplicate Widget ID' errors
                st.link_button(f"📁 Buy Document Folder for {name}", "https://topdeal.in/your-link")
                st.caption("This link refers to Amazon India website.")
                st.info("As an Amazon Associate, I earn from qualifying purchases.")
                st.divider()

        if not found_any:
            st.warning("No matching schemes found for your inputs.")

with tab2:
    st.title("Transparency & Legal")
    st.markdown(f"""
    **DPDP Act 2025 Compliance:**
    - **Data Privacy**: We do not store your age or income inputs.
    - **Affiliate Disclosure**: We use affiliate links to sustain this research.
    - **Status**: This is a private portal, not an official Government site.
    
    *Updated: {datetime.now().strftime('%d %B %Y')}*
    """)
