import streamlit as st
import json
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# Initialize session state for results so they don't disappear on rerun
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

# --- 2. TABS FOR STABILITY ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    
    # Language selector inside the tab to avoid global disturbance
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
    
    # Input Form
    with st.form("main_finder"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submit_btn = st.form_submit_button("SEARCH SCHEMES", use_container_width=True)
        
        if submit_btn:
            st.session_state.search_clicked = True

    # Display results only if search was clicked
    if st.session_state.search_clicked:
        st.success("Results for Age: {} | Income: ₹{}".format(age, income))
        
        # --- SCHEME DISPLAY AREA ---
        # Example Scheme Card
        st.markdown("### UP Scholarship Scheme")
        st.write("Benefit: ₹5000 per year")
        
        # --- COMPLIANT AD SECTION ---
        with st.expander("🛠️ Recommended Resources"):
            st.link_button("📁 Buy Document Folder", "https://topdeal.in/your-link")
            st.caption("This link will refer you to Amazon website for buying.")
            st.info("As an Amazon Associate, I earn from qualifying purchases.")
        
        # Reset button to clear search
        if st.button("Clear Search Results"):
            st.session_state.search_clicked = False
            st.rerun()

with tab2:
    st.title("Privacy Policy & Legal")
    st.markdown(f"""
    **DPDP Act 2025 Compliance:**
    - This is a private information portal.
    - We use affiliate tracking cookies for EarnKaro and Amazon.
    - As an Amazon Associate, I earn from qualifying purchases.
    - Contact: `your-email@gmail.com`
    
    *Last Updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 3. PERMANENT FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>Private Portal | Not Government Official | 2026</p>", unsafe_allow_html=True)
