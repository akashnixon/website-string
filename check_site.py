import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage

URL = "https://www.concordia.ca/hr/jobs/openings/exam-invigilation.html"
TARGET_TEXT = "fall 2025"

def check_website():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return TARGET_TEXT.lower() in soup.get_text().lower()
    except Exception as e:
        print(f"Error checking website: {e}")
        return False

def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.environ["EMAIL_USER"]
    msg['To'] = os.environ["RECEIVER_EMAIL"]
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        smtp.send_message(msg)

if check_website():
    print("✅ 'fall 2025' FOUND — sending email...")
    send_email(
        subject="✅ 'fall 2025' Found on Concordia Invigilation Page!",
        body=f"Visit the site: {URL}"
    )
else:
    print("❌ Not found today.")
