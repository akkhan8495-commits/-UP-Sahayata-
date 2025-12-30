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

# 1. WHATSAPP BUTTON (Fixed Logic)
# We ensure 't' is already defined above in your script
my_num = "919999999999" # REPLACE with your real mobile number
wa_link = f"https://wa.me/{my_num}?text=Help%20with%20UP%20App"

# We use the 't' variable you created at the top of the file
st.link_button(f"💬 {t['wa_button']}", wa_link)

st.divider()

# 2. FEEDBACK SECTION (Visible on Page)
st.subheader(f"📝 {t['feedback_h']}")
with st.form("feedback_form", clear_on_submit=True):
    name_input = st.text_input(t['feedback_n'])
    msg_input = st.text_area(t['feedback_m'])
    submit_btn = st.form_submit_button("Submit")
    
    if submit_btn:
        if msg_input:
            # This confirms the form works! 
            st.success("Dhanyawad! Your feedback is recorded.")
        else:
            st.warning("Please enter a message.")
