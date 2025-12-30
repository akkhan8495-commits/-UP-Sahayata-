import streamlit as st
import json

# Load the data
def load_data():
    with open('schemes.json', 'r') as f:
        return json.load(f)

# Page Setup
st.set_page_config(page_title="UP Sarkari Sahayata", page_icon="🇮🇳")
st.title("🇮🇳 UP Government Scheme Helper")
st.write("Check which government benefits you can get today!")

# User Input Section
st.header("Tell us about yourself")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Your Age", min_value=0, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    income = st.number_input("Annual Family Income (₹)", min_value=0, value=50000)
    is_widow = st.radio("Are you a widow?", ["No", "Yes"])

# Logic Section
if st.button("Find My Schemes"):
    schemes = load_data()
    found = False
    
    st.divider()
    st.subheader("Results for You:")

    for s in schemes:
        eligible = True
        
        # Check Rules
        if "min_age" in s and age < s["min_age"]: eligible = False
        if income > s["max_income"]: eligible = False
        if "gender_target" in s and gender.lower() != s["gender_target"]: eligible = False
        if "target_group" in s and s["target_group"] == "widow" and is_widow == "No": eligible = False

        if eligible:
            found = True
            with st.expander(f"✅ {s['name']}"):
                st.write(f"**Benefit:** {s['benefit']}")
                st.write("**Documents Needed:**")
                for doc in s['docs']:
                    st.write(f"- {doc}")
                st.info("Visit your nearest Jan Seva Kendra to apply.")

    if not found:

        st.error("No schemes found for these details. Please check back later!")

st.divider()

# SAFE FEEDBACK SECTION
st.subheader("📝 Give Feedback / सुझाव दें")

with st.form("feedback_form", clear_on_submit=True):
    name_input = st.text_input("Name (Optional) / नाम")
    msg_input = st.text_area("Message / संदेश")
    submit_btn = st.form_submit_button("Submit / भेजें")
    
    if submit_btn:
        if msg_input:
            import requests
            # This is your unique bridge to the spreadsheet
            FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfazpYpjDE25tlhfAkjc7-U5IgABQFSQw2WKMh2SNvCAAcarg/formResponse"
            
            # Using the exact entry IDs we found for your form
            form_data = {
                "entry.2064104780": name_input,
                "entry.1764614278": msg_input
            }
            
            try:
                requests.post(FORM_URL, data=form_data)
                st.success("Dhanyawad! Check the 'Form Responses 1' tab in your sheet.")
            except:
                st.error("Connection error. Please check your internet.")
        else:
            st.warning("Please enter a message / कृपया संदेश लिखें")
