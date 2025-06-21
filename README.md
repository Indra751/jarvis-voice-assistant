# Jarvis Voice Assistant

A Python-based voice assistant that can perform various tasks through voice commands, including web browsing, music playback, news updates, and AI-powered conversations.

## Features

- **Voice Recognition**: Listens for commands using speech recognition
- **Text-to-Speech**: Responds with voice feedback
- **Web Navigation**: Opens popular websites (Google, YouTube, Instagram, LinkedIn, Facebook)
- **Music Playback**: Plays songs from a predefined library via Spotify
- **News Updates**: Fetches and reads latest news headlines
- **AI Integration**: Uses Google Gemini AI for general queries and conversations
- **Wake Word**: Responds to "Jarvis" wake word

## Prerequisites

- Python 3.7 or higher
- Microphone for voice input
- Internet connection
- API keys for News API and Google Gemini

## Installation

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd jarvis-voice-assistant
   ```

2. **Install required dependencies**
   ```bash
   pip install speech-recognition
   pip install pyttsx3
   pip install requests
   pip install python-dotenv
   pip install google-genai
   pip install pyaudio
   ```

   **Note**: If you encounter issues with `pyaudio`, try:
   - **Windows**: `pip install pipwin && pipwin install pyaudio`
   - **macOS**: `brew install portaudio && pip install pyaudio`
   - **Linux**: `sudo apt-get install python3-pyaudio`

3. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```env
   NEWS_API_KEY=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Get API Keys**
   - **News API**: Register at [newsapi.org](https://newsapi.org/) for a free API key
   - **Google Gemini**: Get your API key from [Google AI Studio](https://aistudio.google.com/)

## Usage

1. **Run the assistant**
   ```bash
   python main.py
   ```

2. **Voice Commands**
   
   Start each command with "Jarvis" followed by your request:

   - **Web Navigation**:
     - "Jarvis, open Google"
     - "Jarvis, open YouTube"
     - "Jarvis, open Instagram"
     - "Jarvis, open LinkedIn"
     - "Jarvis, open Facebook"

   - **Music Playback**:
     - "Jarvis, play [song name]"
     - Available songs: skyfall, levitating, sugar, despacito, faded, dusk till dawn, shape of you, perfect, believer, blinding lights

   - **News**:
     - "Jarvis, news" (reads top 3 headlines about India)

   - **General AI Queries**:
     - "Jarvis, what's the weather like?"
     - "Jarvis, tell me a joke"
     - "Jarvis, explain quantum physics"

   - **Exit**:
     - "Jarvis, goodbye"
     - "Jarvis, stop"
     - "Jarvis, quit"

## Project Structure

```
jarvis-voice-assistant/
├── main.py           # Main application file
├── musicLibrary.py   # Music library with Spotify links
├── .env             # Environment variables (create this)
└── README.md        # This file
```

## File Descriptions

- **main.py**: Core application containing voice recognition, command processing, and AI integration
- **musicLibrary.py**: Dictionary of songs with their Spotify URLs
- **.env**: Environment file for storing API keys securely

## Customization

### Adding New Songs
Edit `musicLibrary.py` to add more songs:
```python
music = {
    "your_song_name": "spotify_url_here",
    # ... existing songs
}
```

### Adding New Commands
Modify the `processcommand()` function in `main.py` to add new voice commands:
```python
elif "your_command" in c.lower():
    # Your custom logic here
    speak("Response message")
```

## Troubleshooting

### Common Issues

1. **Microphone not detected**
   - Check if your microphone is working
   - Try running: `python -m speech_recognition` to test

2. **Speech recognition errors**
   - Ensure stable internet connection
   - Speak clearly and avoid background noise
   - Check microphone permissions

3. **API errors**
   - Verify your API keys are correct in the `.env` file
   - Check API rate limits and quotas

4. **Music not playing**
   - Songs open in web browser; Spotify app should handle playback
   - Ensure song names match exactly (case-insensitive)

### Dependencies Issues
If you encounter import errors, ensure all packages are installed:
```bash
pip install --upgrade pip
pip install -r requirements.txt  # if you create one
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them
- The assistant requires internet access for most features

## Contributing

Feel free to fork this project and add new features such as:
- Calendar integration
- Weather updates
- Smart home controls
- Email management
- Task reminders

## License

This project is open source. Please ensure you comply with the terms of service for all APIs used (News API, Google Gemini, Spotify).

## Acknowledgments

- Google Speech Recognition for voice processing
- News API for news updates
- Google Gemini for AI capabilities
- Spotify for music streaming
