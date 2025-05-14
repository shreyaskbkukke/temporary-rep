import streamlit as st
from src.utils import extract_emails_from_csv, load_smtp_config

st.set_page_config(page_title="Step 1: Load Emails", layout="wide")
st.title("Step 1: Load Email List")

# ---------------------- SMTP Settings Toggle ----------------------
if "smtp_config" not in st.session_state:
    st.session_state.smtp_config = load_smtp_config()

if "show_smtp_settings" not in st.session_state:
    st.session_state.show_smtp_settings = False

def toggle_smtp():
    st.session_state.show_smtp_settings = not st.session_state.show_smtp_settings

if st.button("⚙️ Edit SMTP Settings", on_click=toggle_smtp):
    pass

if st.session_state.show_smtp_settings:
    st.markdown("### SMTP Server Settings")
    cfg = st.session_state.smtp_config
    smtp_server = st.text_input("SMTP Server", value=cfg["smtp_server"], key="smtp_server")
    smtp_port = st.number_input("SMTP Port", value=cfg["smtp_port"], key="smtp_port")
    sender_email = st.text_input("Sender Email", value=cfg["sender_email"], key="sender_email")
    sender_password = st.text_input("Sender Password", type="password", value=cfg["sender_password"], key="sender_password")

    if st.button("Save SMTP Settings"):
        st.session_state.smtp_config = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "sender_email": sender_email,
            "sender_password": sender_password,
        }
        st.success("✅ SMTP settings updated!")
        st.session_state.show_smtp_settings = False  # Auto-collapse

# ---------------------- Email Input Section ----------------------
if "recipients" not in st.session_state:
    st.session_state.recipients = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

upload_file = st.file_uploader("Upload CSV with Email addresses", type=["csv"])
manual_emails = st.text_area("Or paste emails (comma-separated)")

if st.button("Load Emails"):
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
    if st.button("Next: Set Email Content"):
        st.switch_page("pages/Email_Content.py")
