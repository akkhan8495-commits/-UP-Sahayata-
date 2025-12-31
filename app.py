import streamlit as st
import json
import requests

# 1. DATABASE SETUP
def load_data():
    try:
        with open('schemes.json', 'r') as f:
            return json.load(f)
    except:
        return []

st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳")

# Memory to keep results visible
if 'search_active' not in st.session_state:
    st.session_state.search_active = False

# 2. INPUTS
st.title("🇮🇳 UP Scheme Helper")
age = st.number_input("Age / उम्र", min_value=0, value=25)
income = st.number_input("Income / आय", min_value=0, value=50000)

if st.button("Find My Schemes / योजनाएं खोजें"):
    st.session_state.search_active = True

# 3. RESULTS
if st.session_state.search_active:
    schemes = load_data()
    for s in schemes:
        if age >= s.get('min_age', 0) and income <= s['max_income']:
            with st.expander(f"✅ {s['name']}", expanded=True):
                st.info(s['benefit'])
                st.write("---")
                
                # Documents Row
                cols = st.columns(len(s['docs']))
                for i, d in enumerate(s['docs']):
                    with cols[i]:
                        img_url = s.get("doc_images", {}).get(d, "")
                        if img_url:
                            st.image(img_url, width=70)
                        # Checkbox with the document name as the label
                        st.checkbox(d, key=f"chk_{s['name']}_{d}")

# 4. FEEDBACK (Sends to 'Form_Responses' tab)
st.divider()
with st.form("feedback", clear_on_submit=True):
    n = st.text_input("Name / नाम")
    m = st.text_area("Message / संदेश")
    if st.form_submit_button("Submit"):
        if m:
            # Your specific Google Form URL
            url = "https://docs.google.com/forms/d/e/1FAIpQLSfazpYpjDE25tlhfAkjc7-U5IgABQFSQw2WKMh2SNvCAAcarg/formResponse"
            
            # These IDs match the 'entry.' numbers from your pre-filled link
            form_data = {
                "entry.1578076983": n, 
                "entry.518901436": m
            }
            
            try:
                requests.post(url, data=form_data)
                st.success("Success! Your message is now in the Spreadsheet. / सफलता! आपका संदेश स्प्रेडशीट में है।")
            except:
                st.error("Technical Error / तकनीकी खराबी")
        else:
            st.warning("Please enter a message / कृपया संदेश लिखें")
