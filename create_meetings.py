import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
client_id = os.getenv("CLIENT_ID")
account_id = os.getenv("ACCOUNT_ID")
client_secret = os.getenv("CLIENT_SECRET")
gmail_password = os.getenv("GMAIL_PASSWORD")
auth_token_url = "https://zoom.us/oauth/token"
api_base_url = "https://api.zoom.us/v2"
sender_email = "your_email@gmail.com"


def Send_Email(meeting_participants, summary, link):
    receiver_email = meeting_participants[0]['Deepak']
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = summary

    message.attach(MIMEText(link, "plain"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "your_email_password")
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully.")


def Create_Meet(topic, duration, start_date, start_time, host_user_id, attendees_names):
    host_user_id = "275904"
    contacts = []
    with open('contacts.json', 'r') as file:
        contacts = json.loads(file.read())

    meeting_participants = [{contact["name"]: contact["email"]} for contact in contacts if contact["name"] in attendees_names] #filter out attendees
    data = {
        "grant_type": "account_credentials",
        "account_id": account_id,
        "client_secret": client_secret
    }
    
    response = requests.post(auth_token_url,
                             auth=(client_id, client_secret),
                             data=data)

    if response.status_code != 200:
        print("Unable to get access token")
    response_data = response.json()
    access_token = response_data["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "topic": topic,
        "type": 2,
        "start_time": f"{start_date}T{start_time}:00Z",
        "duration": duration,
        "timezone": "Asia/Kolkata",  
        "settings": {
            "join_before_host": True,
            "mute_upon_entry": False,
        },
        "recurrence": {
            "type": 1  
        },
        "host_id": host_user_id,
        "participants": meeting_participants
    }

    resp = requests.post(f"{api_base_url}/users/me/meetings",
                         headers=headers,
                         json=payload)

    if resp.status_code != 201:
        print("Unable to generate meeting link", resp)
    else:
        response_data = resp.json()
        if "join_url" in response_data:
            content = {
                "meeting_url": response_data["join_url"],
                "password": response_data["password"],
                "meetingTime": response_data["start_time"],
                "purpose": response_data["topic"],
                "duration": response_data["duration"],
                "message": "Success",
                "status": 1
            }
            print(content)
            print(meeting_participants)
            Send_Email(meeting_participants = meeting_participants, summary = topic, link = response_data["join_url"])

        else:
            print("Missing 'join_url' in the API response.")


