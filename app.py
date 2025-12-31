import streamlit as st
import json
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- 2. TABS (Stable Layout) ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    
    # Language Selection
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
    
    # Search Form
    with st.form("search_form"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submitted = st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True)

    if submitted:
        try:
            with open('schemes.json', 'r', encoding='utf-8') as f:
                schemes = json.load(f)
            
            found_count = 0
            
            # --- THE LOOP: Checks Every Scheme ---
            for i, s in enumerate(schemes):
                if age >= s['min_age'] and income <= s['max_income']:
                    found_count += 1
                    
                    # Get translated content
                    name = s.get('name_hindi' if lang == "Hindi" else 'name', s['name'])
                    benefit = s.get('benefit_hindi' if lang == "Hindi" else 'benefit', s['benefit'])
                    
                    # Display Scheme Info
                    st.success(f"### {name}")
                    st.write(f"**Benefit:** {benefit}")
                    
                    # --- AFFILIATE SECTION ---
                    # Rechecked: We use a unique label for EACH button to avoid crashes
                    st.link_button(f"📁 Buy Document Folder for {name}", "https://topdeal.in/your-link")
                    st.caption("This link will refer you to Amazon website for buying.")
                    
                    st.info("As an Amazon Associate, I earn from qualifying purchases.")
                    st.divider()

            if found_count == 0:
                st.info("No matching schemes found for your age/income.")
            else:
                st.balloons() # Visual confirmation of success

        except Exception as e:
            st.error(f"Error loading schemes: {e}")

with tab2:
    # --- PRIVACY & COMPLIANCE SECTION ---
    st.title("Privacy Policy & Legal Terms")
    st.markdown(f"""
    **DPDP Act 2025 Compliance:**
    - **No Data Storage**: Your age and income are processed locally and not stored.
    - **Affiliate Disclosure**: This app uses EarnKaro and Amazon affiliate links. 
    - **Earnings**: As an Amazon Associate, I earn from qualifying purchases.
    - **Contact**: `your-email@gmail.com`
    
    *Updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 3. PERMANENT FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>Private Portal | Not Government Official | 2026</p>", unsafe_allow_html=True)
