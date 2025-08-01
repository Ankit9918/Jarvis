import pyttsx3
import speech_recognition as sr
import datetime
import cv2
# import time
import os
# text to speech
def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices[0].id)  # david voice 
    engine.setProperty('voice', voices[0].id)  # ✅ Fix: 'voice' (not 'voices')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

# convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:  # ✅ Fix: r.Microphone() not r.Microphone
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=2, phrase_time_limit=10)  # ✅ Fix: r.listen not sr.listen
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')  # ✅ Fix: recognize_google (not recognize.google), 'language' spelling
        print(f'user said : {query}')
        speak(query)
    except Exception as e:
        speak('say this again please...')
        return "none"
    return query

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
                os.startfile(os.path.join(music_dir, songs[0]))
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye, sir!")
            break
        
    # takecommand()
    # speak('this is advance jarvis')
