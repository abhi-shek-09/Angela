import speech_recognition as sr
from datetime import datetime, timedelta
from create_reminders import Create_Event
from create_meetings import Create_Meet
host_user_id = "275904"

def format(command_list, attendees = True):
    time_str, day_or_night, date_str, month_str = command_list[4:8] # split up everything to access one by one

    if 'th' in date_str or 'rd' in date_str: #format the date and extract the number 
        date_str = date_str[0]
    time_str = time_str.split(':') #split it into hours and minutes

    start_time = datetime(
        2023, 
        datetime.strptime(month_str, "%B").month, #extracting the number of the month
        int(date_str), 
        int(time_str[0]),
        int(time_str[1]), 
        0
    )

    if day_or_night == 'p.m.':
        start_time += timedelta(hours = 12) #adding 12 to the time for p.m.

    summary = command_list[8:]
    if attendees: 
        summary, attendees_list = summary.split('participants')
        attendees_names = attendees_list.split(' ')[1:]
        return [start_time, summary, attendees_names]
    return [start_time, summary]


listener = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print('Listening..')
        voice = listener.listen(source = source) #Continuously listens to a voice
        command = listener.recognize_google(voice) #speech to text
        command_list = command.split(' ')
        meeting_phrases = {'create', 'meet', 'setup', 'meeting'}
        add_to_calendar_phrases = {'add', 'event','to', 'calendar'}

        if command_list[0] == 'Angela':
            #add an event 8:00 a.m. 9 December My Birthday
            if any(phrase in add_to_calendar_phrases for phrase in command_list[1:4]):
                print(command)
                start_time, summary = format(command_list = command_list, attendees = False)
                Create_Event(start_time = start_time, summary = " ".join(summary))
            
            #setup a meet 8:00 p.m. 9 December Discussion on Current Affairs
            elif command_list[1:4] == ['setup', 'a', 'meet'] or command_list[1:4] == ['setup', 'a', 'meeting']:
                start_time, summary, attendees_names = format(command_list = command_list)
                date_string = start_time.strftime('%Y-%m-%d')
                time_string = start_time.strftime('%H:%M:%S')
                print(summary, "60", date_string, time_string, host_user_id, attendees_names)
                Create_Meet(summary, "60", date_string, time_string, host_user_id, attendees_names)

except:
    pass