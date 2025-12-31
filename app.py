import streamlit as st
import json
from datetime import datetime

# --- 1. SETTINGS & SECURITY SHIELD ---
# This must be the very first Streamlit command
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# This CSS hides the GitHub icon, "Manage App" button, and header from users
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
        # Pulls data from the 'Secrets' tab you set up in the dashboard
        # Format in Secrets should be: SCHEME_DATA = ''' [your json] '''
        return json.loads(st.secrets["SCHEME_DATA"])
    except Exception:
        st.error("Data connection is private. Please check Secrets configuration.")
        return []

# --- 3. STABLE TABS ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Search Portal")
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)

    with st.form("main_search"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submitted = st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True)

    if submitted:
        schemes = get_data()
        found_any = False
        
        # This loop checks every entry in your secret data
        for i, s in enumerate(schemes):
            if age >= s['min_age'] and income <= s['max_income']:
                found_any = True
                name = s.get('name_hindi' if lang == "Hindi" else 'name', s['name'])
                benefit = s.get('benefit_hindi' if lang == "Hindi" else 'benefit', s['benefit'])
                
                # Professional Scheme Card
                st.success(f"### {name}")
                st.write(f"**Benefit:** {benefit}")
                
                # Affiliate Links with UNIQUE labels to prevent 'Duplicate ID' errors
                st.link_button(f"📁 Buy Document Folder for {name}", "https://topdeal.in/your-link")
                st.caption("This link refers to Amazon India.")
                st.info("As an Amazon Associate, I earn from qualifying purchases.")
                st.divider()

        if not found_any:
            st.warning("No matching schemes found. Try different criteria.")

with tab2:
    st.title("Transparency & Legal")
    st.markdown(f"""
    **DPDP Act 2025 Compliance Notice:**
    - **Data**: We do not store your age or income inputs.
    - **Affiliates**: This portal uses affiliate links to support its research.
    - **Official Status**: We are a private information provider, not the Government.
    
    *Portal last updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 4. FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>Private Information Portal | 2026</p>", unsafe_allow_html=True)
