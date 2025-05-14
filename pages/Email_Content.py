import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Step 2: Email Content", layout="wide")
st.title("Step 2: Email Content Setup")

if "subject" not in st.session_state:
    st.session_state.subject = os.getenv("SUBJECT")

if "html_content" not in st.session_state:
    st.session_state.html_content = ""

st.session_state.subject = st.text_input("Email Subject", value=st.session_state.subject)

html_file = st.file_uploader("Upload HTML File", type=["html"])
default_html_path = "/home/shreyas/Documents/PythonFile/internship-mail/templates/index.html"

if html_file:
    try:
        st.session_state.html_content = html_file.read().decode("utf-8")
        st.success("Custom HTML file loaded.")
    except Exception as e:
        st.error(f"Error reading HTML: {str(e)}")
elif os.path.exists(default_html_path) and not st.session_state.html_content:
    with open(default_html_path, "r", encoding="utf-8") as f:
        st.session_state.html_content = f.read()
        st.info("ℹ Using default HTML template.")

if st.session_state.subject and st.session_state.html_content:
    if st.button("Next: Start Sending"):
        st.switch_page("pages/Compose_and_Send.py")

else:
    st.warning("Please enter subject and upload or load HTML content.")
