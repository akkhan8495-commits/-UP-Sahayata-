import streamlit as st
import json
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="UP Sahayata | Private Portal",
    page_icon="🇮🇳",
    layout="centered"
)

# --- 2. LANGUAGE DATA ---
texts = {
    "English": {
        "nav_home": "Scheme Finder",
        "nav_privacy": "Privacy & Legal",
        "title": "🇮🇳 UP Sahayata | Private Info Portal",
        "warning": "⚠️ **Legal Disclaimer**: This is a Private Portal. We are NOT affiliated with the Government of UP or India. Please verify data on official sites.",
        "age_label": "Enter Age",
        "income_label": "Annual Income (₹)",
        "button": "SEARCH SCHEMES",
        "results": "Eligible Schemes For You",
        "no_results": "No schemes found. Try lower income or different age.",
        "docs_header": "Required Documents",
        "ad_header": "🛠️ Recommended Resources",
        "ad_sub": "To help with your application, we recommend these tools:",
        "ad_disclaimer": "This link will refer you to Amazon website for buying.",
        "amazon_info": "As an Amazon Associate, I earn from qualifying purchases.",
        "footer": "Private Portal | Not Government Official | DPDP Act 2025 Compliant"
    },
    "Hindi": {
        "nav_home": "योजना खोजें",
        "nav_privacy": "गोपनीयता और कानूनी",
        "title": "🇮🇳 यूपी सहायता | निजी सूचना पोर्टल",
        "warning": "⚠️ **कानूनी अस्वीकरण**: यह एक निजी पोर्टल है। हम यूपी या भारत सरकार से संबद्ध नहीं हैं। कृपया आधिकारिक साइटों पर डेटा सत्यापित करें।",
        "age_label": "उम्र दर्ज करें",
        "income_label": "वार्षिक आय (₹)",
        "button": "योजनाएं खोजें",
        "results": "आपके लिए पात्र योजनाएं",
        "no_results": "कोई योजना नहीं मिली। कृपया कम आय या अलग उम्र दर्ज करें।",
        "docs_header": "जरूरी दस्तावेज",
        "ad_header": "🛠️ सहायक सामग्री",
        "ad_sub": "आपके आवेदन में सहायता के लिए, हम इन उपकरणों की अनुशंसा करते हैं:",
        "ad_disclaimer": "यह लिंक आपको खरीदारी के लिए अमेज़न वेबसाइट पर ले जाएगा।",
        "amazon_info": "एक अमेज़न एसोसिएट के रूप में, मैं योग्य खरीदारी से कमाता हूँ।",
        "footer": "निजी पोर्टल | सरकारी आधिकारिक नहीं | DPDP एक्ट 2025 के अनुरूप"
    }
}

# --- 3. SIDEBAR NAVIGATION & LANGUAGE ---
st.sidebar.title("Menu / मेनू")
lang = st.sidebar.radio("Select Language / भाषा चुनें", ["English", "Hindi"])
t = texts[lang]

# Navigation Pages
page = st.sidebar.selectbox("Go to / यहाँ जाएँ", [t["nav_home"], t["nav_privacy"]])

# --- 4. CUSTOM STYLING ---
st.markdown(f"""
    <style>
    .stNumberInput label {{ font-size: 20px !important; font-weight: bold !important; color: #003366 !important; }}
    .scheme-card {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border-left: 10px solid #ff9933;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333333;
        color: #cccccc;
        text-align: center;
        padding: 8px;
        font-size: 12px;
        z-index: 100;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. PAGE LOGIC: SCHEME FINDER ---
if page == t["nav_home"]:
    st.title(t["title"])
    st.warning(t["warning"])

    # High Visibility Form
    with st.form("input_form"):
        st.subheader("Check Eligibility / पात्रता जांचें")
        age = st.number_input(t["age_label"], min_value=0, max_value=120, value=25)
        income = st.number_input(t["income_label"], min_value=0, value=50000, step=5000)
        submitted = st.form_submit_button(t["button"], use_container_width=True)

    if submitted:
        try:
            with open('schemes.json', 'r', encoding='utf-8') as f:
                schemes = json.load(f)
        except:
            schemes = []
            st.error("Error: schemes.json not found!")

        found = False
        st.header(t["results"])
        
        for s in schemes:
            if age >= s['min_age'] and income <= s['max_income']:
                found = True
                name = s['name_hindi'] if lang == "Hindi" else s['name']
                benefit = s['benefit_hindi'] if lang == "Hindi" else s['benefit']
                
                st.markdown(f"""
                <div class="scheme-card">
                    <h3 style='margin:0; color:#003366;'>{name}</h3>
                    <p style='color:#1e7e34; font-weight:bold; font-size:1.1em;'>{benefit}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Documents Expander
                with st.expander(t["docs_header"]):
                    cols = st.columns(3)
                    for i, doc in enumerate(s['docs']):
                        img = s['doc_images'].get(doc, "https://img.icons8.com/color/144/document.png")
                        cols[i%3].image(img, width=60, caption=doc)
                
                # ADVERTISING / AFFILIATE SECTION
                with st.expander(t["ad_header"]):
                    st.write(t["ad_sub"])
                    
                    # Ad 1: Folder (Replace with your actual EarnKaro/Amazon link)
                    st.link_button("📁 Buy Document Folder", "https://topdeal.in/your-link")
                    st.caption(t["ad_disclaimer"])
                    
                    st.divider()
                    
                    # Ad 2: Book (Replace with your actual EarnKaro/Amazon link)
                    st.link_button("📚 CCC Computer Course Book", "https://topdeal.in/your-link")
                    st.caption(t["ad_disclaimer"])
                    
                    st.info(t["amazon_info"])
        
        if not found:
            st.info(t["no_results"])

# --- 6. PAGE LOGIC: PRIVACY & LEGAL ---
elif page == t["nav_privacy"]:
    st.title("Privacy Policy & Legal")
    st.markdown(f"""
    ### 1. Data Protection (DPDP Act 2025)
    This app is a **private information portal**. We do not store your age, income, or any personal identity data on our servers.
    
    ### 2. Affiliate Disclosure
    This site participates in the Amazon Associates Program via EarnKaro. 
    {t['amazon_info']} All links marked as recommendations will refer you to the Amazon India website.
    
    ### 3. Cookies
    We use standard affiliate tracking cookies to ensure we receive a commission for referrals. This does not increase the price for the user.
    
    ### 4. Verification
    Users are advised to verify all scheme details at [up.gov.in](https://up.gov.in) before applying.
    
    *Last Updated: {datetime.now().strftime('%d %B %Y')}*
    """)

# --- 7. FOOTER ---
st.markdown(f"<div class='footer'>{t['footer']} | {datetime.now().strftime('%Y')}</div>", unsafe_allow_html=True)
