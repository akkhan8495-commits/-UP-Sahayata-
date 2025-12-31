import streamlit as st
import json
import requests

if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

if st.button(t['button']):
    st.session_state.search_clicked = True

if st.session_state.search_clicked:
    # Place all your Scheme Search Logic (the loops) here

# 1. DATABASE SETUP
def load_data():
    try:
        with open('schemes.json', 'r') as f:
            return json.load(f)
    except:
        return []

# 2. CONFIGURATION
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳")

text = {
    "English": {
        "title": "UP Government Scheme Helper",
        "sub": "Find benefits for you and your family",
        "age": "Your Age",
        "income": "Annual Family Income (₹)",
        "gender": "Gender",
        "widow": "Are you a widow?",
        "athlete": "Are you an Athlete?",
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
        "athlete": "क्या आप खिलाड़ी हैं?",
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
# Create a space for results that stays visible
results_container = st.container()

if st.button(t['button']):
    schemes = load_data()
    found = False
    
    with results_container: # This keeps everything inside the box
        for s in schemes:
            eligible = True
            if "min_age" in s and age < s['min_age']: eligible = False
            if income > s['max_income']: eligible = False
            
            if eligible:
                found = True
                with st.expander(f"✅ {s['name']}", expanded=True): # Keeps it open
                    st.info(f"**Benefit:** {s['benefit']}")
                    
                    st.write(f"### {t['docs']}")
                    doc_cols = st.columns(len(s['docs']))
                    
                    for i, d in enumerate(s['docs']):
                        with doc_cols[i]:
                            if "doc_images" in s and d in s["doc_images"]:
                                # Added use_column_width to make sure it displays
                                st.image(s["doc_images"][d], width=80, caption=d) # Added 'caption'
                            st.checkbox(d, key=f"chk_{s['name']}_{d}") # Unique key

# 5. SAFE FEEDBACK SECTION
st.divider()
st.subheader(f"📝 {t['feedback_h']}")

with st.form("feedback_form", clear_on_submit=True):
    name_input = st.text_input(t['feedback_n'])
    msg_input = st.text_area(t['feedback_m'])
    submit_btn = st.form_submit_button("Submit")
    
    if submit_btn:
        if msg_input:
            # Your Google Form Bridge 
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
        else:
            st.warning("Please enter a message.")


