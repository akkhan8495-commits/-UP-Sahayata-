import streamlit as st
import json
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. CONFIG & SECURITY SHIELD ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- ADMITAD VERIFICATION CODE ---
components.html(
    """
    <meta name="verify-admitad" content="0f34354b86" />
    """,
    height=0,
)

# Hides all developer buttons from public users
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# --- 2. FAIL-SAFE DATA LOADER ---
def load_data():
    # Attempt 1: Load from Cloud Secrets
    if "SCHEME_DATA" in st.secrets:
        try:
            return json.loads(st.secrets["SCHEME_DATA"])
        except:
            pass
    
    # Attempt 2: Load from local file if Secrets fail
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# --- 3. INTERFACE ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)

    with st.form("main_search"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submitted = st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True)

    if submitted:
        schemes = load_data()
        if not schemes:
            st.error("Data source not found. Please check your JSON or Secrets.")
        else:
            found = False
            for i, s in enumerate(schemes):
                if age >= s['min_age'] and income <= s['max_income']:
                    found = True
                    name = s.get('name_hindi' if lang == "Hindi" else 'name', s['name'])
                    st.success(f"### {name}")
                    st.write(f"**Benefit:** {s.get('benefit', 'Details on official site')}")
                    
                    # UNIQUE LABEL prevents the 'TypeError' you had earlier
                    st.link_button(f"📁 Get Document Folder for {name}", "https://topdeal.in/your-link")
                    st.caption("Referral to Amazon India. As an associate, I earn from qualifying purchases.")
                    st.divider()
            
            if not found:
                st.info("No matching schemes found.")

with tab2:
    st.title("Legal & Privacy")
    st.markdown(f"**Updated:** {datetime.now().strftime('%d %B %Y')}")
    st.write("This is a private information portal compliant with DPDP Act 2025.")


