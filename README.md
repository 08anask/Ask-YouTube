# Ask-YouTube 🎥🤖

An interactive web application that allows users to ask questions about YouTube video content using AI-powered analysis of video subtitles.

![Ask-YouTube](https://img.shields.io/badge/Ask-YouTube-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Overview

Ask-YouTube is a Flask-based web application that extracts subtitles from YouTube videos and uses AI language models to answer questions about the video content. The application supports multiple AI providers including:

- Google Gemini
- OpenAI (ChatGPT)
- Ollama (for local AI models)

## ✨ Features

- Extract subtitles from any YouTube video with captions
- Process video content using advanced AI models
- Support for multiple AI providers (Gemini, OpenAI, Ollama)
- Save conversation history in session
- User-friendly web interface
- Secure API key management

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/08anask/Ask-YouTube.git
   cd ask-youtube
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. If you want to use Ollama, make sure it's installed on your system. Visit [Ollama's official website](https://ollama.ai/) for installation instructions.

## 🚀 Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter a YouTube URL with available subtitles
4. Select your preferred AI provider and model
5. Ask questions about the video content

## 🔑 API Key Setup

For Gemini and OpenAI, you'll need to provide your API keys:

1. Click on the "API Key Settings" button in the navigation bar
2. Select the AI model provider
3. Enter your API key
4. Save the settings

Note: Ollama runs locally and doesn't require an API key.

## 📂 Project Structure

```
ask-youtube/
├── README.md
├── app.py                # Main application file
├── requirements.txt      # Required Python packages
└── templates/            # HTML templates
    ├── index.html        # Main UI
    └── settings.html     # API key configuration
```

## 🧩 How It Works

1. The application extracts subtitles from YouTube videos using yt-dlp
2. The extracted text is processed by the selected AI model via LangChain
3. Users can ask questions about the video content
4. The AI generates responses based on the video's subtitles
5. Conversation history is stored in the session

## 🔄 Supported AI Models

### Gemini
- Gemini 1.5 Pro
- Gemini 1.5 Flash
- Gemini 2.0 Flash

### OpenAI
- GPT-3.5 Turbo
- GPT-4o Mini
- O3 Mini
- O1 Mini
- GPT-4o

### Ollama
- Any locally installed Ollama model

## 🛠️ Technologies Used

- **Flask**: Web framework
- **yt-dlp**: YouTube subtitle extraction
- **LangChain**: AI model integration
- **Bootstrap**: Frontend styling
- **JavaScript**: Dynamic UI updates

## 📚 Dependencies

- Flask
- yt-dlp
- requests
- json5
- openai
- langchain
- langchain-community
- langchain-google-genai
- langchain-openai
- ollama

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Limitations

- Only works with YouTube videos that have subtitles (auto-generated or manual)
- API key required for Gemini and OpenAI
- Response quality depends on the accuracy of video subtitles and AI model capabilities

## 📬 Contact

For questions or feedback, please open an issue on the repository or contact the project maintainer.

---
