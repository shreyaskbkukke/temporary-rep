import streamlit as st
from src.utils import extract_emails_from_csv

st.set_page_config(page_title="Step 1: Load Emails", layout="wide")
st.title("📧 Step 1: Load Email List")

if "recipients" not in st.session_state:
    st.session_state.recipients = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

upload_file = st.file_uploader("Upload CSV with Email addresses", type=["csv"])
manual_emails = st.text_area("Or paste emails (comma-separated)")

if st.button("📥 Load Emails"):
    if upload_file:
        st.session_state.recipients = extract_emails_from_csv(upload_file)
    elif manual_emails:
        st.session_state.recipients = [e.strip() for e in manual_emails.split(",") if e.strip()]
    else:
        st.warning("Please upload or paste at least one email.")
        st.stop()

    st.success(f"Loaded {len(st.session_state.recipients)} email(s).")
    st.session_state.current_index = 0

if st.session_state.recipients:
    st.write(st.session_state.recipients)
    if st.button("➡️ Next: Set Email Content"):
        st.switch_page("pages/Email_Content.py")
