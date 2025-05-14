import streamlit as st
from datetime import date
from src.smtp_client import SMTPClient
from src.utils import load_smtp_config

st.set_page_config(page_title="Step 3: Send Emails", layout="wide")
st.title("Step 3: Compose & Send")

# ---------------------- Validate State ----------------------
if "recipients" not in st.session_state or not st.session_state.recipients:
    st.error("No email list loaded. Go to Step 1 first.")
    st.stop()

if "html_content" not in st.session_state or not st.session_state.html_content:
    st.error("No email content found. Go to Step 2 first.")
    st.stop()

if "subject" not in st.session_state or not st.session_state.subject:
    st.error("Subject missing. Go to Step 2.")
    st.stop()

recipients = st.session_state.recipients
i = st.session_state.get("current_index", 0)

if i >= len(recipients):
    st.success("All emails processed.")
    st.stop()

# ---------------------- Basic Details ----------------------
recipient_email = recipients[i]
subject = st.session_state.subject
html_content = st.session_state.html_content

# ---------------------- Default Values ----------------------
default_name = recipient_email.split("@")[0].capitalize()
default_from_date = st.session_state.get("default_from", date(2024, 6, 1))
default_to_date = st.session_state.get("default_to", date(2024, 6, 30))

# ---------------------- Editable Fields ----------------------
st.markdown("### ✏️ Personalize Email Content")
name = st.text_input("Name", value=default_name)
from_date = st.date_input("From Date", value=default_from_date)
to_date = st.date_input("To Date", value=default_to_date)

# Save for reuse in next loop
st.session_state.default_from = from_date
st.session_state.default_to = to_date

# ---------------------- Render Personalized Email ----------------------
personalized_html = (
    html_content
    .replace("{{name}}", name)
    .replace("{{from_date}}", str(from_date))
    .replace("{{to_date}}", str(to_date))
)

# ---------------------- Show Recipient ----------------------
st.markdown(f"### Current recipient: `{recipient_email}`")

col1, col2 = st.columns(2)

# ---------------------- Send Button ----------------------
if col1.button("✅ Send Email"):
    try:
        cfg = load_smtp_config()
        client = SMTPClient(
            cfg["smtp_server"],
            cfg["smtp_port"],
            cfg["sender_email"],
            cfg["sender_password"]
        )
        client.send_html_email([recipient_email], subject, personalized_html)
        st.success(f"Email sent to {recipient_email}")
    except Exception as e:
        st.error(f"❌ Failed to send: {e}")
    st.session_state.current_index += 1
    st.rerun()

# ---------------------- Skip Button ----------------------
if col2.button("⏭️ Skip"):
    st.session_state.current_index += 1
    st.rerun()
