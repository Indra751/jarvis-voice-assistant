# 🤖 Jarvis Voice Assistant

A sophisticated Python-based voice assistant powered by Google's Gemini AI that can perform various tasks through voice commands including web browsing, music playback, news updates, and intelligent conversations.

## ✨ Features

- **🎤 Voice Recognition**: Advanced speech recognition with ambient noise adjustment
- **🔊 Text-to-Speech**: Natural voice responses with configurable speech settings
- **🧠 AI Integration**: Powered by Google Gemini 2.0 Flash for intelligent conversations
- **🌐 Web Control**: Open popular websites with voice commands
- **🎵 Music Playbook**: Play songs from a curated library via Spotify
- **📰 News Updates**: Get latest news by category (general, tech, sports, business, entertainment)
- **⏰ Time & Date**: Voice queries for current time and date
- **🎯 Wake Word**: Responds to "Jarvis" wake word activation
- **📝 Comprehensive Logging**: Detailed logging for debugging and monitoring

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Microphone access
- Internet connection
- Google Gemini API key
- NewsAPI key (optional, for news features)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

#### Getting API Keys:

**Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into your `.env` file

**News API Key (Optional):**
1. Visit [NewsAPI](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 4. Install System Dependencies

**Windows:**
```bash
# Install PyAudio dependencies
pip install pyaudio
```

**macOS:**
```bash
# Install PortAudio
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev python3-dev
pip install pyaudio
```

## 🚀 Usage

### Basic Usage

```bash
python Main.py
```

The assistant will initialize and say "Jarvis is now online and ready to assist you!"

### Voice Commands

Start any command with **"Jarvis"** followed by your request:

#### 🌐 Website Commands
- "Jarvis, open Google"
- "Jarvis, open YouTube"
- "Jarvis, open Instagram"
- "Jarvis, open LinkedIn"
- "Jarvis, open Facebook"
- "Jarvis, open Twitter"
- "Jarvis, open Reddit"

#### 🎵 Music Commands
- "Jarvis, play Skyfall"
- "Jarvis, play Levitating"
- "Jarvis, play Shape of You"
- "Jarvis, play Despacito"

#### 📰 News Commands
- "Jarvis, news" (general news)
- "Jarvis, tech news"
- "Jarvis, sports news"
- "Jarvis, business news"
- "Jarvis, entertainment news"

#### ⏰ Time & Date
- "Jarvis, what time is it?"
- "Jarvis, what's the date?"

#### 🧠 AI Conversations
- "Jarvis, explain quantum physics"
- "Jarvis, tell me a joke"
- "Jarvis, how do I learn Python?"
- "Jarvis, what's the weather like?" (AI will respond based on general knowledge)

#### 🛑 Exit Commands
- "Jarvis, goodbye"
- "Jarvis, stop"
- "Jarvis, quit"
- "Jarvis, exit"

## 🏗️ Project Structure

```
jarvis-voice-assistant/
├── Main.py                 # Main voice assistant application
├── Ai_agent_module.py      # AI client module for Gemini integration
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
├── jarvis.log             # Application logs (auto-generated)
└── README.md              # This file
```

## 📋 Requirements

Create a `requirements.txt` file:

```txt
speechrecognition==3.10.0
pyttsx3==2.90
requests==2.31.0
python-dotenv==1.0.0
google-generativeai==0.3.2
pyaudio==0.2.11
```

## ⚙️ Configuration

### Speech Recognition Settings

Adjust these parameters in `Main.py` for better performance:

```python
self.recognizer.energy_threshold = 4000  # Microphone sensitivity
self.recognizer.pause_threshold = 0.8    # Pause detection
```

### Text-to-Speech Settings

Configure voice properties:

```python
self.engine.setProperty('rate', 180)     # Speech speed
self.engine.setProperty('volume', 0.9)   # Volume level
```

### Adding New Songs

Extend the music library in `Main.py`:

```python
self.music_library = {
    "song_name": "spotify_url_here",
    # Add more songs...
}
```

## 🔧 Troubleshooting

### Common Issues

**Microphone Not Working:**
- Check microphone permissions
- Test microphone with other applications
- Adjust `energy_threshold` in code

**API Key Errors:**
- Verify API keys in `.env` file
- Check API key validity and quotas
- Ensure proper environment variable loading

**Audio Issues:**
- Install/reinstall PyAudio
- Check system audio drivers
- Try different TTS voice settings

**Module Import Errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Debug Mode

Enable detailed logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent conversation capabilities
- SpeechRecognition library for voice input processing
- pyttsx3 for text-to-speech functionality
- NewsAPI for news integration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/jarvis-voice-assistant/issues) section
2. Create a new issue with detailed information
3. Include log files and error messages

## 🔮 Future Enhancements

- [ ] Smart home device integration
- [ ] Weather API integration
- [ ] Calendar and reminder functionality
- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Voice command history
- [ ] Plugin architecture for extensibility

---

**Made with ❤️ by Indrajit Biswas**
