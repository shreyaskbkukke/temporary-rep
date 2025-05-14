import pandas as pd
from dotenv import load_dotenv
import os


def extract_emails_from_csv(file) -> list[str]:
    df = pd.read_csv(file)
    return df.iloc[:, 0].dropna().tolist() 


def load_smtp_config():
    load_dotenv()

    return {
        "smtp_server": os.getenv("SMTP_SERVER"),
        "smtp_port": int(os.getenv("SMTP_PORT")),
        "sender_email": os.getenv("SENDER_EMAIL"),
        "sender_password": os.getenv("SENDER_PASSWORD"),
        
        "email_subject": os.getenv("SENDER_PASSWORD"),
    }
