#  Import Required Libraries
import pyttsx3  # for text-to-speech
import speech_recognition as sr  # for speech-to-text
import datetime  # to get current time
import cv2  # to use webcam
import random  # for random music choice
from requests import get  # to fetch IP and geo data
import wikipedia  # to fetch info from Wikipedia
import pywhatkit as kit  # for WhatsApp messaging and YouTube playback
import time  # for delay
import webbrowser  # to open websites
import os  # for OS commands
import smtplib  # to send emails
import sys  # to exit the program
import instaloader  # to download Instagram profile picture
import pyjokes  # for telling jokes
import pyautogui  # for taking screenshots
from dotenv import load_dotenv  # to load email credentials from .env
import requests  # used for IP location tracking

#  Load Environment Variables
load_dotenv()

#  Text-to-speech function
def speak(audio):
    engine = pyttsx3.init('sapi5')  # Initialize speech engine
    voices = engine.getProperty('voices')  # Get voice options
    engine.setProperty('voice', voices[1].id)  # Select female voice
    engine.setProperty('rate', 150)  # Set speech rate
    engine.setProperty('volume', 1.0)  # Max volume
    print(audio)
    engine.say(audio)
    engine.runAndWait()

#  Speech-to-text function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1  # Wait for 1 second pause in speech
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=10)  # Listen for max 10 sec
        except sr.WaitTimeoutError:
            speak("You didn't speak in time. Please try again.")
            return "none"
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')  # Recognize using Google API
        print(f'User said: {query}')
    except Exception:
        speak('Say that again please...')
        return "none"
    return query.lower()

#  Greet the user
def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('Good morning!')
    elif 12 <= hour < 18:
        speak('Good afternoon!')
    else:
        speak('Good evening!')
    speak('I am Jarvis Sir. Please tell me how can I help you.')

#  Send an email using SMTP
def sendemail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP
        server.ehlo()
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))  # Secure login
        server.sendmail(os.getenv("EMAIL_USER"), to, content)
        server.close()
        speak("Email has been sent.")
    except Exception as e:
        print(e)
        speak("Sorry sir, I was unable to send the email.")

#  Main logic loop
if __name__ == '__main__':
    wish()  # Greet user
    while True:
        query = takecommand().lower()
        if query == "none":
            continue

        #  Basic desktop commands
        if 'open notepad' in query:
            os.startfile("C:\\Windows\\notepad.exe")
        elif 'open command prompt' in query:
            os.system('start cmd')
        elif 'open camera' in query:
            # Open the webcam
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('Webcam', img)
                if cv2.waitKey(50) == 27:  # ESC to quit
                    break
            cap.release()
            cv2.destroyAllWindows()

        #  Play music
        elif 'play music' in query:
            music_dir = "C:\\Users\\hp\\Music"
            songs = [file for file in os.listdir(music_dir) if file.lower().endswith(('.mp3', '.wav'))]
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                speak("No music files found.")

        #  Check IP address
        elif 'ip address' in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP Address is {ip}")

        #  Wikipedia search
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            speak(results)

        #  Open websites
        elif 'open youtube' in query:
            webbrowser.open('https://www.youtube.com')
        elif 'open facebook' in query:
            webbrowser.open('https://www.facebook.com')
        elif 'open instagram' in query:
            webbrowser.open('https://www.instagram.com')
        elif 'open stackoverflow' in query:
            webbrowser.open('https://stackoverflow.com')
        elif 'open brave' in query:
            webbrowser.open('https://brave.com')

        #  Google search
        elif 'open google' in query:
            speak('Sir, what should I search on Google?')
            cm = takecommand().lower()
            if cm != "none":
                webbrowser.open(f"https://www.google.com/search?q={cm}")

        #  Send WhatsApp message
        elif 'send message' in query:
            hour = int(datetime.datetime.now().hour)
            minute = int(datetime.datetime.now().minute) + 2
            kit.sendwhatmsg('+919305830375', 'This is a testing protocol', hour, minute)

        #  Play YouTube song
        elif 'play songs on youtube' in query:
            kit.playonyt('see you again')

        #  Email
        elif 'send email' in query:
            speak('What should I say?')
            content = takecommand().lower()
            if content != "none":
                sendemail("rasusahu18092003@gmail.com", content)

        #  Joke
        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        #  System controls
        elif 'shut down the system' in query:
            os.system('shutdown /s /t 5')
        elif 'restart the system' in query:
            os.system('shutdown /r /t 5')
        elif 'sleep the system' in query:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

        #  Location tracking by IP
        elif 'where i am' in query or 'where we are' in query:
            speak('Wait sir, let me check.')
            try:
                ipAdd = get('https://api.ipify.org').text
                url = f'http://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                geo_data = requests.get(url).json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"Sir, I think we are in {city} city of {country} country.")
            except Exception as e:
                speak("Sorry sir, I am unable to find the location due to a network issue.")

        #  Instagram profile viewer & downloader
        elif 'instagram profile' in query or 'profile on instagram' in query:
            speak('Sir, please enter the username correctly.')
            name = input('Enter Instagram username: ')
            webbrowser.open(f'https://www.instagram.com/{name}')
            speak(f'Sir, here is the profile of {name}.')
            time.sleep(5)
            speak('Would you like to download the profile picture of this account?')
            condition = takecommand().lower()
            if 'yes' in condition:
                loader = instaloader.Instaloader()
                loader.download_profile(name, profile_pic_only=True)
                speak('Profile picture downloaded successfully.')

        #  Screenshot
        elif 'take screenshot' in query:
            speak('Sir, please tell me the name for this screenshot file.')
            name = takecommand().lower()
            if name != "none":
                speak('Please hold the screen, taking screenshot...')
                time.sleep(2)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak('Screenshot taken and saved.')

        #  Exit assistant
        elif 'not thanks' in query or 'stop' in query:
            speak("Goodbye, sir!")
            sys.exit()

        #  Follow-up prompt
        speak("Do you have any other work, sir?")
