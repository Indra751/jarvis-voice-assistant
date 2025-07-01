import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os
import threading
import time
import logging
from typing import Optional, Dict, Any

from google import genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with all necessary components."""
        self._load_environment()
        self._initialize_components()
        self._setup_music_library()
        
    def _load_environment(self):
        """Load environment variables and validate API keys."""
        load_dotenv()
        
        self.newsapi_key = os.getenv("NEWS_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.newsapi_key:
            logger.warning("NEWS_API_KEY not found. News functionality will be disabled.")
        if not self.gemini_api_key:
            logger.error("GEMINI_API_KEY not found. AI functionality will be disabled.")
            
    def _initialize_components(self):
        """Initialize speech recognition, TTS engine, and AI client."""
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust based on environment
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Text-to-Speech
        self.engine = pyttsx3.init()
        self._configure_tts()
        
        # AI Client
        if self.gemini_api_key:
            try:
                self.client = genai.Client(api_key=self.gemini_api_key)
                logger.info("Gemini AI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            self.client = None
            
        # State management
        self.is_listening = False
        self.should_quit = False
        
    def _configure_tts(self):
        """Configure text-to-speech settings for better performance."""
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                        
            # Set speech rate and volume
            self.engine.setProperty('rate', 180)  # Slightly faster
            self.engine.setProperty('volume', 0.9)
            
        except Exception as e:
            logger.warning(f"TTS configuration failed: {e}")
            
    def _setup_music_library(self):
        """Setup music library with improved song matching."""
        self.music_library = {
            "skyfall": "https://open.spotify.com/track/6VObnIkLVruX4UVyxWhlqm",
            "levitating": "https://open.spotify.com/track/39LLxExYz6ewLAcYrzQQyP",
            "sugar": "https://open.spotify.com/track/2iuZJX9X9P0GKaE93xcPjk",
            "despacito": "https://open.spotify.com/track/6habFhsOp2NvshLv26DqMb",
            "faded": "https://open.spotify.com/track/7BKLCZ1jbUBVqRi2FVlTVw",
            "dusk till dawn": "https://open.spotify.com/track/3e7sxremeOE3wTySiOhGiP",
            "shape of you": "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3",
            "perfect": "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v",
            "believer": "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP",
            "blinding lights": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
        }
        
        # Create aliases for better song matching
        self.song_aliases = {
            "dusk till dawn": ["dusk till dawn", "dusk to dawn", "dusk until dawn"],
            "shape of you": ["shape of you", "shape of u"],
            "blinding lights": ["blinding lights", "blinding light"],
        }

    def speak(self, text: str, async_mode: bool = False):
        """Enhanced speak function with threading support."""
        if not text:
            return
            
        logger.info(f"Speaking: {text}")
        
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
            
    def _speak_sync(self, text: str):
        """Synchronous speak function."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")

    def ai_process(self, command: str) -> str:
        """Process command using AI with better error handling and caching."""
        if not self.client:
            return "AI functionality is not available. Please check your API key."
            
        try:
            # Add context for better responses
            enhanced_prompt = f"""
            You are Jarvis, a helpful voice assistant. Respond concisely and naturally.
            User query: {command}
            
            Keep responses brief and conversational for voice interaction.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",  # Use the latest model
                contents=enhanced_prompt,
            )
            
            # Clean up response
            cleaned_response = response.text.replace("*", "").strip()
            logger.info(f"AI Response: {cleaned_response[:100]}...")
            
            return cleaned_response
            
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            return "I'm having trouble processing that request right now."

    def find_song(self, song_query: str) -> Optional[str]:
        """Enhanced song matching with fuzzy search."""
        song_query = song_query.lower().strip()
        
        # Direct match
        if song_query in self.music_library:
            return self.music_library[song_query]
            
        # Check aliases
        for song, aliases in self.song_aliases.items():
            if song_query in aliases:
                return self.music_library[song]
                
        # Partial match
        for song_name in self.music_library:
            if song_query in song_name or song_name in song_query:
                return self.music_library[song_name]
                
        return None

    def get_news(self, category: str = "general", country: str = "in") -> bool:
        """Fetch and speak news with better error handling."""
        if not self.newsapi_key:
            self.speak("News service is not configured.")
            return False
            
        try:
            url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={self.newsapi_key}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            if not articles:
                self.speak("No news articles found at the moment.")
                return False
                
            self.speak(f"Here are the top {min(3, len(articles))} headlines:")
            
            for i, article in enumerate(articles[:3], 1):
                title = article.get('title', 'No title available')
                self.speak(f"News {i}: {title}")
                time.sleep(0.5)  # Brief pause between headlines
                
            return True
            
        except requests.exceptions.Timeout:
            self.speak("News service is taking too long to respond.")
            logger.error("News API timeout")
            return False
        except requests.exceptions.RequestException as e:
            self.speak("I'm having trouble connecting to the news service.")
            logger.error(f"News API error: {e}")
            return False
        except Exception as e:
            self.speak("An error occurred while fetching news.")
            logger.error(f"Unexpected news error: {e}")
            return False

    def process_command(self, command: str) -> str:
        """Enhanced command processing with better organization."""
        command = command.lower().strip()
        
        if not command:
            return "continue"
            
        logger.info(f"Processing command: {command}")
        
        # Website commands
        website_commands = {
            "open google": ("https://google.com", "Opening Google"),
            "open youtube": ("https://youtube.com", "Opening YouTube"),
            "open instagram": ("https://instagram.com", "Opening Instagram"),
            "open linkedin": ("https://linkedin.com", "Opening LinkedIn"),
            "open facebook": ("https://facebook.com", "Opening Facebook"),
            "open twitter": ("https://twitter.com", "Opening Twitter"),
            "open reddit": ("https://reddit.com", "Opening Reddit"),
        }
        
        for cmd, (url, message) in website_commands.items():
            if cmd in command:
                self.speak(message)
                webbrowser.open(url)
                return "continue"
        
        # Music commands
        if command.startswith("play"):
            song_query = command.replace("play", "").strip()
            
            if not song_query:
                self.speak("Please specify a song to play.")
                return "continue"
                
            song_url = self.find_song(song_query)
            
            if song_url:
                self.speak(f"Playing {song_query}")
                webbrowser.open(song_url)
            else:
                self.speak(f"Sorry, I couldn't find {song_query} in my music library.")
                # Fallback to YouTube search
                youtube_search = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"
                self.speak("Let me search for it on YouTube instead.")
                webbrowser.open(youtube_search)
                
            return "continue"
        
        # News commands
        if "news" in command:
            if "technology" in command or "tech" in command:
                self.get_news("technology")
            elif "sports" in command:
                self.get_news("sports")
            elif "business" in command:
                self.get_news("business")
            elif "entertainment" in command:
                self.get_news("entertainment")
            else:
                self.get_news("general")
            return "continue"
        
        # Time and date commands
        if "time" in command:
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            return "continue"
            
        if "date" in command:
            current_date = time.strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            return "continue"
        
        # Exit commands
        exit_commands = ["goodbye", "stop", "quit", "exit", "bye"]
        if any(exit_cmd in command for exit_cmd in exit_commands):
            self.speak("Goodbye! Have a great day!")
            return "quit"
        
        # AI processing for everything else
        self.speak("Let me think about that...")
        response = self.ai_process(command)
        self.speak(response)
        
        return "continue"

    def listen_for_command(self) -> Optional[str]:
        """Enhanced listening with better error handling and calibration."""
        try:
            with sr.Microphone() as source:
                if not self.is_listening:
                    logger.info("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    self.is_listening = True
                
                logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
                logger.info("Processing speech...")
                command = self.recognizer.recognize_google(audio)
                
                return command.lower()
                
        except sr.WaitTimeoutError:
            logger.debug("Listening timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected listening error: {e}")
            return None

    def run(self):
        """Main loop with improved error handling and user experience."""
        self.speak("Jarvis is now online and ready to assist you!")
        self.speak("Say 'Jarvis' followed by your command.")
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while not self.should_quit:
            try:
                command = self.listen_for_command()
                
                if command is None:
                    consecutive_errors += 1
                    if consecutive_errors >= max_consecutive_errors:
                        logger.warning("Too many consecutive listening errors")
                        self.speak("I'm having trouble hearing you. Please check your microphone.")
                        time.sleep(2)
                        consecutive_errors = 0
                    continue
                
                consecutive_errors = 0  # Reset error counter on successful recognition
                
                if command.startswith("jarvis"):
                    # Remove "jarvis" wake word and process command
                    actual_command = command.replace("jarvis", "").strip()
                    
                    if actual_command:
                        logger.info(f"Wake word detected. Command: {actual_command}")
                        result = self.process_command(actual_command)
                        
                        if result == "quit":
                            self.should_quit = True
                            break
                    else:
                        self.speak("Yes, how can I help you?")
                        
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                self.speak("Shutting down...")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    self.speak("I'm experiencing technical difficulties. Restarting...")
                    time.sleep(3)
                    consecutive_errors = 0

def main():
    """Main entry point."""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"Failed to start voice assistant: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()