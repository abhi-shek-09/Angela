import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("../Api keys/google_calendar.json", SCOPES)
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    
    # now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    # print("Getting the upcoming 10 events")
    # events_result = (
    #     service.events()
    #     .list(
    #         calendarId="primary",
    #         timeMin=now,
    #         maxResults=10,
    #         singleEvents=True,
    #         orderBy="startTime",
    #     )
    #     .execute()
    # )
    # events = events_result.get("items", [])

    # if not events:
    #   print("No upcoming events found.")
    #   return

    # # Prints the start and name of the next 10 events
    # for event in events:
    #   start = event["start"].get("dateTime", event["start"].get("date"))
    #   print(start, event["summary"])



    events = {
      "summary" : "My birthday",
      "location" : "NYC",
      "description": "My bday through api call",
      "colorId": 6,
      "start":{
        "dateTime": "2023-12-09T00:00:00+02:00",
        "timeZone": "Asia/Kolkata"
      },
      "end":{
        "dateTime": "2023-12-09T01:00:00+02:00",
        "timeZone": "Asia/Kolkata"
      },
      "recurrence":[
        "RRULE: FREQ=DAILY; COUNT=1"
      ],
      "attendees":[
        {"email": "abhishekmurthy364@gmail.com"}
      ]
    }

    event = service.events().insert(calendarId = "primary", body= events).execute()
    print(f"event created {event.get('htmlLink')}")
    

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()