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

# 2. CONFIGURATION & MEMORY
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳")

# This "memory" keeps the results on screen when checkboxes are clicked
if 'results_visible' not in st.session_state:
    st.session_state.results_visible = False

text = {
    "English": {
        "title": "UP Government Scheme Helper",
        "sub": "Find benefits for you and your family",
        "age": "Your Age",
        "income": "Annual Family Income (₹)",
        "gender": "Gender",
        "widow": "Are you a widow?",
        "button": "Find My Schemes",
        "docs": "Required Documents (Checklist):",
        "feedback_h": "Give Feedback",
        "feedback_n": "Name",
        "feedback_m": "Suggestions/Message"
    },
    "हिन्दी": {
        "title": "UP सरकारी योजना सहायक",
        "sub": "अपने परिवार के लिए सरकारी लाभ खोजें",
        "age": "आपकी उम्र",
        "income": "वार्षिक आय (₹)",
        "gender": "लिंग",
        "widow": "क्या आप विधवा हैं?",
        "button": "योजनाएं खोजें",
        "docs": "आवश्यक दस्तावेज (चेकलिस्ट):",
        "feedback_h": "सुझाव दें",
        "feedback_n": "नाम",
        "feedback_m": "आपका संदेश"
    }
}

lang = st.sidebar.selectbox("Select Language", ["English", "हिन्दी"])
t = text[lang]

st.title(f"🇮🇳 {t['title']}")
st.write(t['sub'])

# 3. USER INPUTS
col1, col2 = st.columns(2)
with col1:
    age = st.number_input(t['age'], min_value=0, value=25)
    gender = st.selectbox(t['gender'], ["Male", "Female", "Other"])
with col2:
    income = st.number_input(t['income'], min_value=0, value=50000)
    is_widow = st.radio(t['widow'], ["No", "Yes"])

# 4. SEARCH LOGIC
if st.button(t['button']):
    st.session_state.results_visible = True

if st.session_state.results_visible:
    schemes = load_data()
    found = False
    for s in schemes:
        eligible = True
        if "min_age" in s and age < s['min_age']: eligible = False
        if income > s['max_income']: eligible = False
        
        if eligible:
            found = True
            with st.expander(f"✅ {s['name']}", expanded=True):
                st.info(f"**Benefit:** {s['benefit']}")
                st.write(f"### {t['docs']}")
                
                # FEATURE: Document Images with Captions for clarity
                doc_cols = st.columns(len(s['docs']))
                for i, d in enumerate(s['docs']):
                    with doc_cols[i]:
                        if "doc_images" in s and d in s["doc_images"]:
                            # width=90 and caption makes it easier to understand
                            st.image(s["doc_images"][d], width=90, caption=d)
                        st.checkbox("Ready", key=f"chk_{s['name']}_{d}")
                
                st.warning("Visit your nearest Jan Seva Kendra with these documents.")

    if not found:
        st.error("No schemes found for your profile.")

# 5. SAFE FEEDBACK SECTION (Sends to 'Form Responses 1' tab)
st.divider()
st.subheader(f"📝 {t['feedback_h']}")

with st.form("feedback_form", clear_on_submit=True):
    name_input = st.text_input(t['feedback_n'])
    msg_input = st.text_area(t['feedback_m'])
    submit_btn = st.form_submit_button("Submit")
    
    if submit_btn:
        if msg_input:
            # This links to your specific Google Form and Spreadsheet
            FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfazpYpjDE25tlhfAkjc7-U5IgABQFSQw2WKMh2SNvCAAcarg/formResponse"
            form_data = {
                "entry.2064104780": name_input,
                "entry.1764614278": msg_input
            }
            try:
                requests.post(FORM_URL, data=form_data)
                st.success("Dhanyawad! Your message is in the 'Form Responses 1' tab.")
            except:
                st.error("Error connecting to sheet.")
