import streamlit as st
import json
import requests

# --- 1. CONFIG & DATA ---
st.set_page_config(page_title="UP Sahayata", page_icon="🇮🇳", layout="wide")

def load_data():
    try:
        with open('schemes.json', 'r') as f:
            return json.load(f)
    except:
        return []

# --- 2. CUSTOM CSS FOR CARDS ---
st.markdown("""
    <style>
    .scheme-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .benefit-text {
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

# --- 4. INPUT SECTION ---
st.title("🇮🇳 UP Scheme Helper | उत्तर प्रदेश योजना सहायक")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Enter Age / उम्र दर्ज करें", min_value=0, max_value=120, value=25)
    with col2:
        income = st.number_input("Annual Income / वार्षिक आय (₹)", min_value=0, value=50000)

    # --- AGE CONFIRMATION LOGIC ---
    if age < 5:
        st.warning("⚠️ Note: You are checking for a minor child. / आप एक छोटे बच्चे के लिए जाँच कर रहे हैं।")
    
    btn_col1, btn_col2 = st.columns([1, 5])
    with btn_col1:
        if st.button("Search / खोजें", type="primary"):
            st.session_state.search_clicked = True
    with btn_col2:
        if st.button("Reset / रीसेट"):
            st.session_state.search_clicked = False
            st.rerun()

st.divider()

# --- 5. RESULTS SHOWING SYSTEM ---
if st.session_state.search_clicked:
    schemes = load_data()
    found_any = False
    
    st.subheader("Eligible Schemes / आपके लिए योजनाएं")
    
    for s in schemes:
        # Filter Logic
        if age >= s.get('min_age', 0) and income <= s.get('max_income', 1000000):
            found_any = True
            
            # Start Card Container
            with st.container():
                st.markdown(f"""
                <div class="scheme-card">
                    <h3>✅ {s['name']}</h3>
                    <p class="benefit-text">Benefit: {s['benefit']}</p>
                    <hr>
                </div>
                """, unsafe_allow_html=True)
                
                # Documents Checklist in Columns inside the expander
                with st.expander("View Required Documents / जरूरी दस्तावेज देखें"):
                    doc_cols = st.columns(4)
                    for idx, doc in enumerate(s['docs']):
                        with doc_cols[idx % 4]:
                            img_url = s.get("doc_images", {}).get(doc, "https://img.icons8.com/color/144/document.png")
                            st.image(img_url, width=60)
                            st.checkbox(doc, key=f"chk_{s['name']}_{doc}")
    
    if not found_any:
        st.error("No schemes found for your criteria. Try adjusting age or income.")

# --- 6. FEEDBACK ---
with st.sidebar:
    st.header("Feedback / फीडबैक")
    with st.form("feedback_form", clear_on_submit=True):
        name = st.text_input("Name")
        msg = st.text_area("Message")
        if st.form_submit_button("Send"):
            # Put your specific entry IDs here
            data = {"entry.1578076983": name, "entry.518901436": msg}
            url = "https://docs.google.com/forms/d/e/1FAIpQLSfazpYpjDE25tlhfAkjc7-U5IgABQFSQw2WKMh2SNvCAAcarg/formResponse"
            requests.post(url, data=data)
            st.success("Thank you!")
