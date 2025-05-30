import streamlit as st

st.set_page_config(page_title="Insight", layout="centered")
st.title("Insight")

hide_sidebar = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

st.markdown("""
Welcome! This app helps you choose the perfect career path based on your interests and skills.

👉 Click the button below to begin the test and start predicting your career.
""")

if st.button("🚀 Start the Aptitude Test"):
    st.switch_page("pages/Aptitude_Test.py")
elif st.button("🚀 Start the Personality Test"):
    st.switch_page("pages/Personality.py")

