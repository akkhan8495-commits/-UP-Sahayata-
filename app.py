import streamlit as st
import json
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="centered")

# --- 2. TABS ---
tab1, tab2 = st.tabs(["🔍 Find Schemes", "⚖️ Privacy & Legal"])

with tab1:
    st.title("🇮🇳 UP Sahayata | Scheme Finder")
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)

    with st.form("input_form"):
        age = st.number_input("Enter Age", 0, 100, 25)
        income = st.number_input("Annual Income (₹)", 0, 1000000, 50000)
        submitted = st.form_submit_button("SEARCH ALL SCHEMES", use_container_width=True)

    if submitted:
        try:
            with open('schemes.json', 'r', encoding='utf-8') as f:
                schemes = json.load(f)
            
            found_any = False
            # THE LOOP: Checks every item in your JSON
            for i, s in enumerate(schemes):
                if age >= s['min_age'] and income <= s['max_income']:
                    found_any = True
                    name = s['name_hindi'] if lang == "Hindi" else s['name']
                    
                    # Scheme Card
                    st.success(f"### {name}")
                    st.write(f"**Benefit:** {s.get('benefit', 'N/A')}")
                    
                    # UNIQUE KEYS (This fixes the TypeError)
                    # We add {i} to make every button's ID different
                    st.link_button(f"📁 Buy Document Folder", "https://topdeal.in/link", key=f"folder_btn_{i}")
                    st.caption("This link will refer you to Amazon website for buying.")
                    
                    st.info("As an Amazon Associate, I earn from qualifying purchases.")
                    st.divider()

            if not found_any:
                st.info("No matching schemes found.")
        except Exception as e:
            st.error(f"Error loading schemes: {e}")

with tab2:
    st.title("Privacy Policy & Legal")
    st.markdown(f"""
    **DPDP Act 2025 Compliance:**
    - Private portal. No data stored.
    - Affiliate links used via EarnKaro/Amazon.
    - Contact: `your-email@gmail.com`
    
    *Last Updated: {datetime.now().strftime('%d %B %Y')}*
    """)
