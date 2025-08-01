import pyttsx3
import speech_recognition as sr
import datetime
import cv2
import random
from requests import get
import wikipedia 
import pywhatkit as kit
import time
import webbrowser
import os
import smtplib
import sys
from instadownloader as instaloader
import pyjokes
# text to speech
def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices[0].id)  # david voice 
    engine.setProperty('voice', voices[1].id)  # ✅ Fix: 'voice' (not 'voices')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

# convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:  
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=2, phrase_time_limit=10)  
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')  
        print(f'user said : {query}')
        speak(query)
    except Exception as e:
        if e == sr.exceptions.WaitTimeoutError:
            speak("You didn't speak in time , please try again. " )
            speak('say this again please...')
        return "none"
    return query.lower()

#to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <=12:
        speak('Good Morning')
    elif hour > 12 and hour < 18:
        speak('good afternoon')
    else:
        speak('good evening') 
    speak('I am jarvis sir , please tell me how can i help you') 

def sendemail( to , content):
    server = smtplib.SMTP('smtp.gmail.com' , 587)
    server.ehlo()
    server.starttls()
    server.login('sahuankit9918@gmail.com' ,'sahu9918@gmail.com')
    server.sendmail('sahuankit9918@gmail.com' , to , content)
    server.close()

if __name__ == '__main__':
    wish()
    while True:
     if 1:

        query = takecommand().lower()
        if 'open notepad' in query:
            print(query)
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)
        elif 'open command prompt' in query:
            os.system('start cmd')   
        elif 'open camera' in query:
            cap = cv2.VideoCapture(0) # 0 for internal camera and 1 for external
            while True:
                ret , img = cap.read()
                cv2.imshow('webcam' , img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()    
            cv2.destroyAllWindows()
        elif 'play music' in query:
                music_dir = "C:\\Users\\hp\\Music"
                songs = os.listdir(music_dir)
                songs = [file for file in os.listdir(music_dir) if file.lower().endswith(('.mp3', '.wav'))]
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))
        elif "ip address" in query:
               ip = get('https://api.ipify.org').text
               speak(f"Your IP Address is {ip}")
        elif "wikipedia" in query:
            speak('searching wikipedia...') 
            query = query.replace('wikipedia',"")
            results = wikipedia.summary(query, sentences = 2)
            speak('according to wikipedia ')
            speak(results)
            print(results)
        elif "open youtube" in query:
            webbrowser.open('www.youtube.com')
        elif "open facebook" in query:
            webbrowser.open('www.facebook.com')   
        elif "open instagram" in query:
            webbrowser.open('www.instagram.com')  
        elif "open stackoverflow" in query:
            webbrowser.open('www.stackoverflow.com')
        elif "open brave" in query:
            webbrowser.open('www.brave.com')       
        elif 'open google' in query:
            speak('sir , what should i search on google')
            cm = takecommand().lower()
            search_query = cm.replace(" ", "+")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")  
            kit.search(search_query)
        elif "send message" in query:
            hour = int(datetime.datetime.now().hour)
            minute = int(datetime.datetime.now().minute)
            kit.sendwhatmsg('+919305830375' ,'this is testing protocol' ,hour,minute + 2 )
        elif 'play songs on youtube' in query:
            kit.playonyt('see you again')    
        elif "send email" in query:
            try:
                speak('what should i say?')
                content = takecommand().lower()
                to = "rasusahu18092003@gmail.com"    
                sendemail(to , content)
                speak('email send to Ankit')
            except Exception as e:
                print(e)
                speak('sorry sir , i am not able to send email')  
        elif 'tell me a joke' in query:  
             joke = pyjokes.get_jokes()
             speak(joke)        
        elif 'shut down the system' in query:
            os.system('shutdown /s /t 5')
        elif 'restart the system' in query:
            os.system('shutdown /r /t 5')   
        elif 'sleep the system' in query:
            os.system('rundll32.exe.poweprof.dil.SetSuspendState 0,1,0') 
        elif 'where i am ' in query or 'where we are' in query:
            speak('wait sir , let me check')
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'http://get.geojs.io/v1/ip/geo/' +ipAdd+'.json'
                geo_requests = requests.get(url)   
                geo_data = geo_requests.json() 
                city = geo_data['city']
                country = geo_data['country']
                speak(f'sir i am not sure , but i think we are in {city} city of{country} country')
            except Exception as e:
                speak('sorry sir , Due to network issue i am not able to find where we are')
                pass

        elif  'instagram Profile' in query or 'profile on instagram' in query:
            speak('sir please enter the user name correctly')
            name = input('Enter username here.')
            webbrowser.open(f'www.instagram.com/{name}')
            speak(f'sir here is the profile of the user')
            time.sleep(5)
            speak('sir would you like to download the profile picture of this account')
            condition = takecommand().lower()
            if 'yes' in condition:
                mod = instaloader.Instaloader() # pip install instadownloader
                mod.download_profile(name , profile_pic_only = True)
                speak(' i am done sir , profile picture is saved in to your main folder')
            else:
                pass;

        elif 'takescreen shot' in query or ' take a screen shot' in query:
            speak('sir please tell me the name for this screenshot file')
            name = takecommand().lower()
            speak('please sir hold the screen for few second, i am taking screenshot')   
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f'{name}.png')
            speak('i am done sir')


        elif 'not thanks' in query or 'stop' in query:
            speak("Goodbye, sir!")
            sys.exit()
        speak('do you have any other work sir!')


    # takecommand()
    # speak('this is advance jarvis')
