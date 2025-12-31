import streamlit as st
import json
from datetime import datetime

# --- 1. SETUP ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# Initialize Search State
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

# --- 2. TABS ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    
    # Language Selection
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
    
    # Input Form
    with st.form("input_area"):
        age = st.number_input("Enter Age / उम्र", 0, 100, 25)
        income = st.number_input("Annual Income / वार्षिक आय (₹)", 0, 1000000, 50000)
        btn = st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True)
        if btn:
            st.session_state.search_clicked = True

    # --- RESULTS LOGIC ---
    if st.session_state.search_clicked:
        try:
            with open('schemes.json', 'r', encoding='utf-8') as f:
                schemes_data = json.load(f)
            
            st.subheader(f"Showing Eligible Schemes for Age {age}")
            
            found_count = 0
            
            # LOOP THROUGH EVERY SCHEME
            for idx, s in enumerate(schemes_data):
                # Check Eligibility
                if age >= s['min_age'] and income <= s['max_income']:
                    found_count += 1
                    
                    # Display Scheme Info
                    name = s['name_hindi'] if lang == "Hindi" else s['name']
                    benefit = s['benefit_hindi'] if lang == "Hindi" else s['benefit']
                    
                    st.markdown(f"""
                    <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; border-left: 5px solid #ff9933; margin-bottom:10px;">
                        <h3 style="margin:0; color:#003366;">{name}</h3>
                        <p style="color:#1e7e34; font-weight:bold;">{benefit}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Required Documents for THIS scheme
                    with st.expander(f"Check Documents for {name}"):
                        for doc in s['docs']:
                            st.write(f"✅ {doc}")
                    
                    # AFFILIATE LINKS (Unique keys ensure all buttons show)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button(f"📁 Buy Document Folder", "https://topdeal.in/your-link", key=f"folder_{idx}")
                        st.caption("Refers to Amazon")
                    with col2:
                        st.link_button(f"📚 CCC Exam Guide", "https://topdeal.in/your-link", key=f"book_{idx}")
                        st.caption("Refers to Amazon")
                    
                    st.divider()

            if found_count == 0:
                st.warning("No schemes found. Try a different age or lower income.")
            else:
                st.success(f"Successfully found {found_count} schemes!")

        except FileNotFoundError:
            st.error("Error: schemes.json file is missing on GitHub!")

with tab2:
    st.title("Privacy Policy & Legal")
    st.markdown(f"""
    ### 1. Transparency (DPDP Act 2025)
    We are a private portal. We do not store your age or income data.
    
    ### 2. Affiliate Disclosure
    This site participates in the Amazon Associates Program. As an Amazon Associate, I earn from qualifying purchases. 
    Clicking 'Buy' links will refer you to the Amazon India website.
    
    ### 3. Contact
    For support, email: `your-email@gmail.com`
    
    *Last Updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 3. FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>Private Information Portal | Not Govt Official | 2026</p>", unsafe_allow_html=True)
