import os
import streamlit as st
from src.smtp_client import SMTPClient
from src.utils import extract_emails_from_csv, load_smtp_config

# Load SMTP config from .env
if "smtp_config" not in st.session_state:
    st.session_state.smtp_config = load_smtp_config()

if "show_settings" not in st.session_state:
    st.session_state.show_settings = False


def toggle_settings():
    st.session_state.show_settings = not st.session_state.show_settings


# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="HTML Email Sender", layout="wide")
st.title("HTML Email Sender")

# ---------------------- SETTINGS MODAL TRIGGER ----------------------
if st.button("⚙️", on_click=toggle_settings):
    pass

# ---------------------- SETTINGS MODAL ----------------------
if st.session_state.show_settings:
    with st.expander("SMTP Settings", expanded=True):
        smtp_server = st.text_input("SMTP Server", value=st.session_state.smtp_config["smtp_server"], key="smtp_server")
        smtp_port = st.number_input("SMTP Port", value=st.session_state.smtp_config["smtp_port"], key="smtp_port")
        sender_email = st.text_input("Sender Email", value=st.session_state.smtp_config["sender_email"], key="sender_email")
        sender_password = st.text_input("Password", type="password", value=st.session_state.smtp_config["sender_password"], key="sender_password")

        if st.button("Save Settings"):
            st.session_state.smtp_config = {
                "smtp_server": smtp_server,
                "smtp_port": smtp_port,
                "sender_email": sender_email,
                "sender_password": sender_password,
            }
            st.success("SMTP settings updated!")
            st.session_state.show_settings = False

# ---------------------- COMPOSE EMAIL ----------------------
st.subheader("Compose Email")
subject = st.text_input("Email Subject")

html_file = st.file_uploader("Upload HTML File for Email Content", type=["html"])
default_html_path = "/home/shreyas/Documents/PythonFile/internship-mail/templates/index.html"
html_content = None

if html_file:
    try:
        html_content = html_file.read().decode("utf-8")
        st.success("Custom HTML file loaded.")
    except Exception as e:
        st.error(f"Failed to read uploaded HTML file: {str(e)}")
elif os.path.exists(default_html_path):
    try:
        with open(default_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            st.info("Using default template: templates/default_template.html")
    except Exception as e:
        st.error(f"Failed to load default HTML template: {str(e)}")
else:
    st.warning("No HTML file uploaded and no default template found.")

# ---------------------- RECIPIENT LIST ----------------------
st.subheader("Recipient List")
upload_file = st.file_uploader("Upload CSV with Email addresses", type=["csv"], key="recipients_csv")
manual_emails = st.text_area("Or paste emails (comma-separated)")

to_emails = []
if upload_file:
    to_emails = extract_emails_from_csv(upload_file)
elif manual_emails:
    to_emails = [email.strip() for email in manual_emails.split(",") if email.strip()]

# ---------------------- SEND EMAIL ----------------------
if st.button("Send Emails"):
    cfg = st.session_state.smtp_config

    if not (cfg["smtp_server"] and cfg["smtp_port"] and cfg["sender_email"] and cfg["sender_password"]):
        st.error("SMTP settings incomplete.")
    elif not (subject and html_content and to_emails):
        st.error("Missing subject, valid HTML content, or recipients.")
    else:
        try:
            client = SMTPClient(cfg["smtp_server"], cfg["smtp_port"], cfg["sender_email"], cfg["sender_password"])
            client.send_html_email(to_emails, subject, html_content)
            st.success(f"Emails sent to {len(to_emails)} recipients.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
