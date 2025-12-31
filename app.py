import streamlit as st
import json
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- 2. THE STABLE TABS ---
# This replaces sidebars and messy buttons at the bottom.
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    # --- YOUR MAIN WORK ---
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
    
    with st.form("main_finder"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submitted = st.form_submit_button("SEARCH SCHEMES", use_container_width=True)

    if submitted:
        st.success("Results loading...")
        # Your affiliate links stay here, safe and clean.
        st.link_button("📁 Buy Document Folder", "https://topdeal.in/your-link")
        st.caption("This link will refer you to Amazon website for buying.")
        st.info("As an Amazon Associate, I earn from qualifying purchases.")

with tab2:
    # --- YOUR POLICY WORK ---
    st.title("Privacy Policy & Legal Terms")
    st.markdown(f"""
    **DPDP Act 2025 Compliance Notice:**
    - We do not store personal data.
    - We use affiliate tracking cookies (Amazon/EarnKaro).
    - For help, contact: `your-email@gmail.com`
    
    *Last Updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 3. CLEAN FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>Private Portal | Not Government Official | 2026</p>", unsafe_allow_html=True)
