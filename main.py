import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
# import threading
from google import genai
# Ensure you have the required libraries installed:
from dotenv import load_dotenv
# Ensure you have a .env file with NEWS_API_KEY set
load_dotenv()  # Load environment variables from .env file

newsapi = os.getenv("NEWS_API_KEY")  # Ensure you have set this environment variable
gemini_api = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = gemini_api)
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=command,
    )
    return(response.text.replace("*",""))

def processcommand(c):

   if "open google" in c.lower():
      speak("Opening Google")
      webbrowser.open("https://google.com")

   elif "open youtube" in c.lower():
      speak("Opening YouTube")
      webbrowser.open("https://youtube.com")

   elif "open instagram" in c.lower():
      speak("Opening Instagram")
      webbrowser.open("https://instagram.com")

   elif "open linkedin" in c.lower():
      speak("Opening LinkedIn")
      webbrowser.open("https://linkedin.com")

   elif "open facebook" in c.lower():
      speak("Opening Facebook")
      webbrowser.open("https://facebook.com")

   elif c.lower().startswith("play"):
      # In processcommand for the music part
      song = c.lower().replace("play", "").strip() 
      link = musicLibrary.music.get(song)
      # ... rest of the logic
      if link:
            webbrowser.open(link)
            speak(f"Alright, playing {song} on spotify")
      elif song:
         speak(f"Sorry, I couldn't find the song {song}.")
      else:
         speak("Please specify a song to play.")
      
   elif "news" in c.lower():
     try:
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={newsapi}")
        r.raise_for_status() 

        data = r.json()
        articles = data.get('articles', [])
        
        # This check is crucial for a good user experience
        if not articles:
            speak("Sorry, I could not find any news articles at this time.")
            return

        speak("Here are the top 3 headlines.")
        for article in articles[:3]:
            speak(article['title'])

     except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I'm having trouble connecting to the news service.")
   
   elif "goodbye" in c.lower() or "stop" in c.lower() or "quit" in c.lower():
       speak("Goodbye! Have a great day!")
       return "quit"
   else:
       speak(f"Loading the answer of {command}")
       output = aiprocess(c)
       speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        # Inside the while loop
        try:
            with sr.Microphone() as source:
                print("Listening for a command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                
                if command.startswith("jarvis"):
                    # Remove "jarvis" from the command
                    command = command.replace("jarvis", "").strip()
                    print(f"User Command: {command}")
                    result = processcommand(command) # Now process the rest of the command
                    if result == "quit":
                        break
                        
                       
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            #speak("Sorry, I could not reach the speech recognition service.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            #speak("Sorry, I did not understand that.")
        except OSError as e:
            print(f"Microphone not found or not working: {e}")
            #speak("Sorry, I could not access the microphone.")
        except Exception as e:
            print(f"Error: {e}")
            #speak("An error occurred.")