import speech_recognition as sr
from datetime import datetime, timedelta
from create_reminders import Create_Event

def Add_Event(command_list):
    try:
        time_str, day_or_night, date_str, month_str = command_list[4:8] # split up everything to access one by one
        summary = command_list[8:] #take the last words as the summary
        
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

        Create_Event(start_time = start_time, summary = " ".join(summary))
    except:
        return "Error processing the command, please try again"


listener = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print('Listening..')
        voice = listener.listen(source = source) #Continuously listens to a voice
        command = listener.recognize_google(voice) #speech to text
        command_list = command.split(' ')
        if command_list[0] == 'Angela':
            if command_list[1:4] == ['add', 'an', 'event'] or command_list[1:4] == ['add', 'to', 'calendar']:
                print(command)
                Add_Event(command_list = command_list) 

except:
    pass