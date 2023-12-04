import speech_recognition as sr

listener = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print('Listening..')
        voice = listener.listen(source = source)
        command = listener.recognize_google(voice)
        print(command)
        if command.split(' ')[0] == 'Angela':
            print(command)

except:
    pass