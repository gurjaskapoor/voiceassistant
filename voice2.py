import speech_recognition as sr
import pyttsx3
import requests
import datetime
import os
import pytz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1)  
def speak(text):
    engine.say(text)
    engine.runAndWait()
print("Assistant: Hello! I'm your personal assistant. How can I help you today?")
speak("Hello! I'm your personal assistant. How can I help you today?")

while True:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Assistant: Please speak something...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-US").lower()
            print("You:", text)
        except sr.UnknownValueError:
            print("Assistant: Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            continue
        except sr.RequestError:
            print("Assistant: Could not connect to the speech recognition service.")
            speak("Could not connect to the speech recognition service.")
            continue

    
    if "weather" in text:
        print("Assistant: Which city do you want the weather for?")
        speak("Which city do you want the weather for?")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            city = recognizer.recognize_google(audio, language="en-US").lower()
            print("You:", city)
        except sr.UnknownValueError:
            print("Assistant: Sorry, I didn't catch that city.")
            speak("Sorry, I didn't catch that city.")
            continue

        api_key = os.getenv("OPENWEATHER_API_KEY", "b5da24c8e06391ac0e080828e775a8d7")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            weather_info = f"The weather in {city.capitalize()} is {weather} with a temperature of {temp}°C."
            print(f"Assistant: {weather_info}")
            speak(weather_info)
        else:
            error_message = "Sorry, I couldn't fetch the weather. Please try again later."
            print("Assistant:", error_message)
            speak(error_message)

    
    elif "news" in text:
        api_key_news = os.getenv("NEWSAPI_KEY", "63f494579e1148a39c94e3ef4bec6943")
        url_news = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key_news}"
        try:
            response = requests.get(url_news)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                headlines = [article['title'] for article in articles[:5]]
                print("Assistant: Here are the top 5 news headlines: ")
                for i, headline in enumerate(headlines, 1):
                    print(f"{i}. {headline}")
                speak("Here are the top 5 news headlines: " + ", ".join(headlines))
            else:
                print("Assistant: Sorry, I couldn't fetch the news.")
                speak("Sorry, I couldn't fetch the news.")
        except requests.exceptions.RequestException:
            print("Assistant: Could not connect to the news service.")
            speak("Could not connect to the news service.")
    
    
    elif "time" in text:
        print("Assistant: What city do you want the time for?")
        speak("What city do you want the time for?")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            city = recognizer.recognize_google(audio, language="en-US").lower()
            print("You:", city)
        except sr.UnknownValueError:
            print("Assistant: Sorry, I didn't catch that city.")
            speak("Sorry, I didn't catch that city.")
            continue
        
        try:
            
            timezone = pytz.timezone(city.capitalize())
            local_time = datetime.datetime.now(timezone).strftime("%I:%M %p")
            time_message = f"The current time in {city.capitalize()} is {local_time}."
            print(f"Assistant: {time_message}")
            speak(time_message)
        except pytz.UnknownTimeZoneError:
            print("Assistant: Sorry, I couldn't find the timezone for that city.")
            speak("Sorry, I couldn't find the timezone for that city.")
    
    
    elif "exit" in text or "quit" in text:
        print("Assistant: Goodbye!")
        speak("Goodbye!")
        break

    
    else:
        response_message = "I'm not sure how to help with that."
        print("Assistant:", response_message)
        speak(response_message)
