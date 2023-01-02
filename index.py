import pyttsx3
import datetime
import smtplib
import speech_recognition as sr
from secret import *
from email.message import EmailMessage
import pyautogui
import webbrowser as web
from time import sleep
import wikipedia
import pywhatkit
import requests
from newsapi import NewsApiClient
import clipboard
import os
import pyjokes
import string
import random
import psutil
from nltk.tokenize import word_tokenize

engine = pyttsx3.init()

# Rate of the speech
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

# setting up volume level  between 0 and 1
# engine.setProperty('volume', 0.82)

# Only given for the choice that voice can be changed with commands also
voices = engine.getProperty('voices')


def setVoice(voice):
    engine.setProperty('voice', voices[voice].id)

# engine.setProperty('voice', voices[0].id)  #0 for male
# engine.setProperty('voice', voices[1].id)   #1 for female
# engine.setProperty('voice', voices[2].id)   #2 for voice girl taken from google


def speak(audio):
    engine.say(audio)
    engine.runAndWait()  # Without this command, speech will not be audible to us


def fullnameofmonth(month):
    if (month == 1):
        return "January"
    elif (month == 2):
        return "February"
    elif (month == 3):
        return "March"
    elif (month == 4):
        return "April"
    elif (month == 5):
        return "May"
    elif (month == 6):
        return "June"
    elif (month == 7):
        return "July"
    elif (month == 8):
        return "August"
    elif (month == 9):
        return "September"
    elif (month == 10):
        return "October"
    elif (month == 11):
        return "November"
    elif (month == 12):
        return "December"

# Date Function


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)

    month = fullnameofmonth(month)
    speak(f"Today is {date}th of {month} {year}")

    if (date == 27 and month == "October"):
        speak("Happy Birthday Sir!")
        speak("It is special day for you")
        speak("How can I make it more special for you?")

# Time Function


def time():
    # Time = datetime.datetime.now().strftime("%I:%M:%S") #I for 12 hour clock
    Time = datetime.datetime.now().strftime("%H:%M:%S")  # H for 24 hour clock
    speak("The current time is:")
    speak(Time)


# Wish me function
def wishme():
    speak("Welcome back sir!")
    # greeting()
    speak("I'm at your service Sir. Please tell me how can I help you?")

# Greeting Function


def greeting():
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning Sir!")
    elif (hour >= 12 and hour < 18):
        speak("Good Afternoon Sir!")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")

# taking command from cmd


def takeCommandCMD():
    query = input("How can I help you Sir? ")
    return query


def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        # for code of all language visit this link
        # https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
        print(query)

    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"

    return query

# How to stop the program


def stop():
    speak("Thank you Sir! Have a nice day!")
    engine.stop()
    exit()


def sendEmail(reciever, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Transport Layer Security(TLS) is a cryptographic protocol that provides communication security over a computer network.
    server.starttls()
    server.login(senderEmail, epwd)

    speak("Sending Email Sir!")
    # server.sendmail(senderEmail,to,'Hello my friend this email is sent by AI Assistant of Nishant, I hope you are doing well.')
    # server.sendmail(senderEmail,to,content)
    email = EmailMessage()
    email['From'] = senderEmail
    email['To'] = to[reciever]
    email['Subject'] = subject
    email.set_content(content)

    server.send_message(email)

    server.close()


def sendWhatsAPPmsg(name, message):
    Message = message
    speak("Opening Whatsapp Web Sir!")
    web.open("https://web.whatsapp.com/send?phone=" +
             phone_no[name]+"&text="+Message)
    speak("Sending Message Sir!")
    sleep(15)
    pyautogui.press("enter")


def wikipediaSearch(query):
    speak("Searching on Wikipedia...")
    query = query.replace("wikipedia", "")
    # sentences = 2 means it will show only 2 sentences
    result = wikipedia.summary(query, sentences=2)
    print(result)
    speak(result)


def searchGoogle():
    speak("What should I search on Google Sir?")
    search = takeCommandMIC()
    web.open("https://www.google.com/search?q="+search)
    speak(f"Here is what I found for {search} on google")


def playonYoutube():
    speak("What should I play on Youtube Sir?")
    topic = takeCommandMIC()
    pywhatkit.playonyt(topic)


def weather():
    city = "Jhajjar"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=bc1e927c77151347ebeea8091a69a8e0"
    res = requests.get(url)
    weatherReport = res.json()
    descri = weatherReport['weather'][0]['description']
    temp = weatherReport['main']['temp']
    temp = round((temp-32)*5/9)
    temp_feel = weatherReport['main']['feels_like']
    temp_feel = round((temp_feel-32)*5/9)
    speak(f"Current temperature in {city} is {temp} degree celsius")
    print(f"Current temperature in {city} is {temp} degree celsius")
    speak(f"but It feels like {temp_feel} degree celsius")
    print(f"but It feels like {temp_feel} degree celsius")
    speak(f"Current weather in {city} is {descri}")
    print(f"Current weather in {city} is {descri}")


def news():
    newsapi = NewsApiClient(api_key='872fa1bb0b7a48898201a139760f23af')

    speak("Sir do you want to hear about specific topic or general news?")
    query = takeCommandMIC()
    if (('general' in query) or ('general news' in query)):
        speak("Here are some top headlines from India")
        newsReport = newsapi.get_top_headlines(language='en', page_size=5)
        newsdata = newsReport['articles']
        for x, y in enumerate(newsdata, 1):
            print(f'{x} {y["description"]} ')
            speak(f'{x} {y["description"]} ')

    elif (('specific' in query) or ('specific news' in query)):
        speak("Sir please tell me the topic")
        specifi_topic = takeCommandMIC()
        newsReport = newsapi.get_everything(
            q=specifi_topic, language='en', page_size=5)
        newsdata = newsReport['articles']
        for x, y in enumerate(newsdata, 1):
            print(f'{x} {y["description"]} ')
            speak(f'{x} {y["description"]} ')

    else:
        speak("Sorry Sir! I am not able to understand what you said")
        speak("I will try toh understand it next time")
        return None

    speak("That's all for now, I'll update you with more news later.")


def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)

def screenshot():
    name_img = int(datetime.datetime.now().timestamp())
    name_img = 'filepath\\name.png'
    img = pyautogui.screenshot(name_img)
    img.show()


def passgenerator():
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation

    passlen = int(input("Enter the length of password: "))
    if (passlen < 8):
        print("Password length should be greater than 8")
        speak("Password length should be greater than 8")
        speak("Please try again")
        passgenerator()

    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))

    random.shuffle(s)
    newpass = ("".join(s[0:passlen]))
    speak("Here is your password")
    print()
    print(newpass)
    print()


def flip():
    speak("Okay Sir, flipping a coin")
    coin = ['Heads', 'Tails']
    toss = random.choice(coin)
    speak(f"I flipped a coin and it's {toss}")


def rollDice():
    speak("Okay Sir, rolling a dice")
    dice = ['1', '2', '3', '4', '5', '6']
    num = random.choice(dice)
    speak(f"I rolled a dice and it's {num}")


def cpu():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percent")
    battery = psutil.sensors_battery()
    speak(f"Battery is at {battery.percent} percent")


def sendwishestofrnds():
    speak("Sir should I send wishes to your friends in message or email?")
    query = takeCommandMIC().lower()
    event = "Happy New Year!!"
    if ('email' in query):
        for key in em:
            speak(f"Sir, Sending wishes to {key}")
            name1 = key.title()
            content = f"Happy New Year 2023✨✨ {name1}, Wishing you health, wealth, and new blessings to count each day in 2023 \n --By Nishant"
            sendEmail(key, event, content)
            speak(f"Wishes sent successfully to {key}")
    else:
        speak("I am not able to understand what you said")
        speak("Please try again")
        sendwishestofrnds()


# Main Function
if __name__ == "__main__":
    wishme()
    # wakeword = 'klaus'
    # speak(wakeword)
    while True:
        query = takeCommandMIC().lower()
        # query = word_tokenize(query)
        # print(query)
        # if wakeword in query:

        if 'time' in query:
            time()

        elif 'date' in query:
            date()

        elif ('send email' in query) or ('send a mail' in query) or ('send mail' in query) or ('send an email' in query):
            try:
                speak("To whom should I send the email?")
                # reciever = takeCommandCMD().lower()
                reciever = input("Enter the name of reciever: ").lower()
                speak("What should be the subject of the email?")
                subject = takeCommandMIC().lower()
                speak("What should I write in the email?")
                content = takeCommandMIC()
                sendEmail(reciever, subject, content)
                speak("Email has been sent successfully Sir!")

            except Exception as e:
                print(e)
                speak("Sorry Sir! I am not able to send this email")

        elif ('whatsapp message' in query) or ('message' in query):
            try:
                speak("To whom should I send the WhatsApp Message?")
                # reciever = takeCommandCMD().lower()
                name = input("Enter the name of reciever: ").lower()
                speak("What should I write in the message?")
                message = takeCommandMIC()
                sendWhatsAPPmsg(name, message)
                speak("Message has been sent successfully Sir!")

            except Exception as e:
                print(e)
                speak("Sorry Sir! I am not able to send this message")

        elif 'wikipedia' in query:
            wikipediaSearch(query)

        elif ('google' in query) or ('search' in query) or ('search on google' in query):
            searchGoogle()

        elif ('open youtube' in query) or ('youtube' in query):
            playonYoutube()

        elif 'weather' in query:
            weather()

        elif ('news' in query) or ('today news' in query):
            news()

        elif ('read clipboard' in query) or ('read clipboard text' in query):
            text2speech()

        elif ('open my folder' in query) or ('open my personal folder' in query):
            # os.system('explorer C://{}'.format(query.replace("open", "")))
            os.system('explorer C:\\Users\\Deepender\\Documents\\Coding\\Nishant')

        elif ('open code' in query) or ('open visual studio code' in query) or ('open vs code' in query):
            codePath = "C:\\Users\\Deepender\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe"
            os.startfile(codePath)

        elif ('joke' in query) or ('tell me a joke' in query):
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif ('screenshot' in query) or ('take screenshot' in query):
            screenshot()

        elif 'remember that' in query:
            speak("What should I remember Sir?")
            r = takeCommandMIC()
            speak("You asked me to remember that " + r)
            remeber = open('data.txt', 'w')
            remeber.write(r)
            remeber.close()

        elif 'do you remember anything' in query:
            remeber = open('data.txt', 'r')
            print(remeber.read())
            remeber.seek(0)
            speak("You asked me to remember that " + remeber.read())
            remeber.close()

        elif 'generate password' in query:
            passgenerator()

        elif ('flip a coin' in query) or ('flip coin' in query):
            flip()

        elif ('roll a dice' in query) or ('roll dice' in query):
            rollDice()

        elif ('cpu' in query) or ('cpu usage' in query):
            cpu()

        elif ('send wishes to friend' in query) or ('send wishes to my friend' in query) or ('wishes to my friend' in query):
            sendwishestofrnds()

        elif ('goodbye' in query) or ('bye' in query) or ('good night' in query) or ('offline' in query):
            stop()
