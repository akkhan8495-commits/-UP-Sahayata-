import streamlit as st
import json
from datetime import datetime

# --- 1. SETUP ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# Initialize state to keep results visible after clicking buttons
if 'results_ready' not in st.session_state:
    st.session_state.results_ready = False

# --- 2. TABS FOR STABILITY ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
    
    with st.form("input_form"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        if st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True):
            st.session_state.results_ready = True
            # We store the inputs to keep them consistent during reruns
            st.session_state.current_age = age
            st.session_state.current_income = income

    # --- RESULTS LOGIC ---
    if st.session_state.results_ready:
        try:
            with open('schemes.json', 'r', encoding='utf-8') as f:
                schemes = json.load(f)
            
            found_any = False
            # LOOP: This checks every single item in your JSON
            for i, s in enumerate(schemes):
                # Using the stored session state values
                if st.session_state.current_age >= s['min_age'] and \
                   st.session_state.current_income <= s['max_income']:
                    
                    found_any = True
                    name = s['name_hindi'] if lang == "Hindi" else s['name']
                    benefit = s['benefit_hindi'] if lang == "Hindi" else s['benefit']
                    
                    # Display the scheme
                    st.success(f"### {name}")
                    st.write(f"**Benefit:** {benefit}")
                    
                    # AFFILIATE SECTION (Crucial: Unique keys using 'i')
                    with st.expander(f"Recommended Tools for {name}"):
                        st.link_button("📁 Buy Folder", "https://topdeal.in/link", key=f"f_{i}")
                        st.caption("Refers to Amazon")
                        st.link_button("📚 Exam Guide", "https://topdeal.in/link", key=f"b_{i}")
                        st.caption("Refers to Amazon")
                    st.divider()

            if not found_any:
                st.info("No matching schemes found. Try adjusting your age or income.")
        except FileNotFoundError:
            st.error("schemes.json not found!")

with tab2:
    st.title("Privacy & Legal")
    st.markdown(f"""
    **DPDP Act 2025 Compliance:**
    - We do not store your personal data.
    - This site uses affiliate links; we earn a commission at no cost to you.
    - As an Amazon Associate, I earn from qualifying purchases.
    - Contact: `your-email@gmail.com`
    *Updated: {datetime.now().strftime('%d %Y')}*
    """)
