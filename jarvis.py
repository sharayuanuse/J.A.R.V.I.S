import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import requests
from plyer import notification
import time
from win10toast import ToastNotifier
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sharayu Anu sey")
    elif hour>=12 and hour<18:
        speak("Good afternoon Sharayu Anu sey")
    else:
        speak("Good evening Sharayu Anu sey")
    speak("I am your personal assistant Jarvis. Please tell me how may i help you?")
def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 2 #seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio,language = 'en-in')
        print(f'User said: {query}\n')
    except Exception as e:
        print('Say that again please...')
        return 'None'
    return query
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('sharayu.anuse@gmail.com','Sharayud@2603')
    server.sendmail('sharayu.anuse@gmail.com',to,content)
    server.close()
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return(f"Weather in {city}: {data['weather'][0]['description']}")
def set_reminder(title, message, delay_str):
    try:
        delay = float(delay_str)
        time.sleep(delay)
        notification.notify(
            title=title,
            message=message,
            app_name="JARVIS",
            timeout=10
        )
    except Exception as e:
        speak('Invalid input for delay')
def display_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10)

if __name__ == '__main__':
    speak("Welcome Sharayu Anu sey")
    wishMe()
    if 1:
        query = takeCommand().lower()
        #Logic for executing taks based in query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia','')
            results = wikipedia.summary(query,sentences = 3)
            speak('According to wikipedia')
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
        elif 'open google' in query:
            webbrowser.open('google.com')
        elif 'open stackoverflow' in query:
            webbrowser.open('stackoverflow.com')
        elif 'play music' in query:
            music_dir = 'C:\\Users\\SHARAYU\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            num = random.randint(1,len(songs)-1)
            os.startfile(os.path.join(music_dir,songs[num]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The time is {strTime}')
        elif 'open code' in query:
            code_path = "D:\Microsoft VS Code\Code.exe"
            os.startfile(code_path)
        elif 'email to sharayu' in query:
            try:
                speak('What should I say?')
                content = takeCommand()
                to = 'sharayu.anuse@gmail.com'
                sendEmail(to,content)
                speak('Email has been sent')
            except Exception as e:
                speak('Sorry yaar Sharayu. I am not able to send this email')
        elif 'quit' in query:
            exit()
        elif 'weather' in query:
            speak('Okay. For Which city do you want to know the weather?')
            city = takeCommand()
            result = get_weather(city)
            speak(result)
        elif 'set a reminder' in query:
            speak("I'll help you in scheduling a reminder")
            speak('Tell me the title of your task')
            title = takeCommand()
            speak('What is the message you want to set for yourself')
            message = takeCommand()
            speak('After how much time should i remind you about your task')
            delay = takeCommand()
            set_reminder(title,message,delay)
            #speak(result)
        elif 'notification' in query:
            speak('Tell me the title of your task')
            title = takeCommand()
            speak('What is the message you want to set for yourself')
            message = takeCommand()
            display_notification(title,message)
