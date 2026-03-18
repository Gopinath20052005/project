# 📄 AI PDF Reader & Translator

An intelligent web application built with Python and Flask that allows users to upload a PDF, translate its content into multiple languages, and listen to it with natural AI voice narration.

## 🚀 Features

* 📄 Upload and read PDF files
* 🌍 Translate text into multiple languages
* 🔊 Convert translated text into speech
* 🎧 Natural AI voice reader
* ⏱️ Word-by-word highlighting during playback
* 📱 Mobile-friendly interface

## 🧠 Supported Languages

* English
* Tamil
* Hindi
* Malayalam

## 🛠️ Technologies Used

* Python
* Flask
* PyPDF2 (PDF text extraction)
* Google Translator
* Text-to-Speech (AI voice generation)
* HTML, CSS, JavaScript

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/pdf-reader-ai.git
```

2. Navigate to the project folder

```bash
cd pdf-reader-ai
```

3. Install dependencies

```bash
pip install flask PyPDF2 gtts googletrans==4.0.0-rc1
```

4. Run the application

```bash
python app.py
```

5. Open in browser

```
http://localhost:5000
```

## 📂 Project Workflow

1. User uploads a PDF file
2. Text is extracted from the PDF
3. Text is translated into the selected language
4. Audio is generated from the translated text
5. User can listen to the PDF with synchronized text highlighting

## 🎯 Future Improvements

* Faster AI voice engine
* More language support
* PDF page highlighting
* Mobile app version
* Advanced AI summarization

├── requirements.txt          # Python dependencies
├── run.bat                   # Windows batch script
├── run.ps1                   # PowerShell script
│
├── templates/                # HTML templates
│   ├── login.html           # Login page
│   └── home.html            # Main application page
│
├── static/                   # Static files
│   ├── css/
│   │   ├── login.css        # Login page styling
│   │   └── home.css         # Application styling
│   │
│   └── js/
│       └── home.js          # Application logic & events
│
├── uploads/                  # PDF upload directory
├── audio_output/            # Generated MP3 files
│
├── README.md                # This file
├── SETUP.md                 # Setup instructions
├── DEPLOYMENT.md            # Deployment guide
├── PROJECT_OVERVIEW.md      # Project documentation
└── TROUBLESHOOTING.md       # Troubleshooting guide
```

## 🔌 API Endpoints

### POST `/api/upload-pdf`
Upload and extract text from PDF
- **Request**: Form data with PDF file and language
- **Response**: Extracted text, available languages

### POST `/api/translate-text`
Translate extracted text
- **Request**: JSON with text and target language
- **Response**: Translated text

### POST `/api/convert-text`
Convert text to MP3 audio
- **Request**: JSON with text, language, voice
- **Response**: Audio file path and URL

### GET `/audio/<filename>`
Stream audio file
- **Response**: MP3 audio stream

### GET `/download-audio/<filename>`
Download audio file
- **Response**: MP3 file download

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Supported languages
SUPPORTED_LANGUAGES = ['Tamil', 'English', 'Hindi', 'Malayalam']

# Maximum file size (50MB default)
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

# Audio quality (False = normal, True = slow/clear)
AUDIO_SLOW_MODE = False

# Debug mode
DEBUG = True

# Server settings
HOST = '127.0.0.1'
PORT = 5000
```

## 🔒 Security Features

- **File Upload Validation** - Only PDF files allowed
- **File Size Limits** - Maximum 50MB per upload
- **Secure Filename Handling** - UUID-based naming
- **XSS Protection** - HTML escaping for user input
- **CSRF Protection** - Built into Flask forms
- **Automatic Cleanup** - Optional old file deletion

## 🚀 Performance Tips

1. **For Large PDFs**:
   - System automatically pages large PDFs
   - Text extraction is optimized
   - Consider breaking into smaller sections

2. **For Faster Conversion**:
   - Use English language (fastest)
   - Shorter text = faster generation
   - Male voice may be slightly faster

3. **For Better Audio Quality**:
   - Use gTTS with normal mode (not slow)
   - Female voice offers natural tone
   - Check internet connection for TTS

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows: Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### PDF Extraction Issues
- Ensure PDF is text-based (not image-based)
- Try splitting large PDFs
- Check PDF isn't password-protected

### Translation Errors
- Verify internet connection
- Check supported languages
- Restart application

### Audio Generation Fails
- Verify gTTS installation
- Check internet for TTS service
- Try shorter text snippets

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help.

## 📝 Supported Languages

| Language | Code | Conversion Available |
|----------|------|---------------------|
| Tamil    | ta   | ↔ English, Hindi, Malayalam |
| English  | en   | ↔ Tamil, Hindi, Malayalam |
| Hindi    | hi   | ↔ Tamil, English, Malayalam |
| Malayalam| ml   | ↔ Tamil, English, Hindi |

## 🎨 Customization

### Change Colors
Edit `static/css/home.css` - Update the gradient colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add More Languages
Edit `config.py` and add language mappings:
```python
LANGUAGE_CODES = {
    'YourLanguage': 'language_code'
}
```

### Modify Voice Options
Edit `static/js/home.js` - Expand voice selection dropdown

## 📊 Limitations

- Maximum PDF size: 50MB
- Translation depends on Google Translate (requires internet)
- Audio generation depends on gTTS (requires internet)
- Processing time varies based on text length
- Voice limitations based on gTTS capabilities

## 🔄 Updates & Maintenance

- Check for library updates regularly
- Monitor disk space for audio files
- Clean up old audio files periodically
- Test with various PDF formats
- Update dependencies: `pip install -r requirements.txt --upgrade`

## 📄 License

This project is created for educational and personal use.

## 👥 Support & Contact

For issues or questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
3. Check application console for error messages

## 🎉 Features Roadmap

Future enhancements may include:
- ✅ Real-time word highlighting during playback
- ✅ PDF page-by-page processing
- ✅ Side-by-side text comparison
- ✅ Multiple voice options
- ✅ Playback speed control
- 📋 User accounts and history
- 📋 Batch PDF processing
- 📋 Custom voice settings
- 📋 More language options
- 📋 Cloud integration

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Status**: Fully Functional ✅

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📂 Project Structure

```
PDF TO AUDIO READER/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── login.html        # Login page
│   └── home.html         # Home/main page
├── static/
│   ├── css/
│   │   ├── login.css     # Login page styles
│   │   └── home.css      # Home page styles
│   └── js/
│       └── home.js       # JavaScript functionality
├── uploads/              # Uploaded PDF files (temporary)
├── audio_output/         # Generated audio files (MP3)
└── backend/              # Backend utilities (if needed)
```

## 🎨 User Interface

### Login Page
- Welcome screen with "Let's Get Started" button
- Quick feature overview

### Home Page
1. **Upload Section**: Drag-and-drop PDF upload with language selection
2. **Text Preview**: Shows extracted text from PDF
3. **Conversion Section**: Select target language and voice
4. **Audio Player**: Built-in player with controls
5. **Download Option**: Save generated audio file

## 🌍 Supported Languages

| Input Language | Can Convert To |
|---|---|
| Tamil | English, Hindi, Malayalam |
| English | Tamil, Hindi, Malayalam |
| Malayalam | Tamil, English, Hindi |
| Hindi | Tamil, English, Malayalam |

## 🎤 Voice Options

- **Female Voice** (Default)
- **Male Voice**

## 📝 Usage Steps

1. **Open Application**: Navigate to `http://localhost:5000`
2. **Click "Let's Get Started"**: Proceed to home page
3. **Upload PDF**: Drag and drop or click to select PDF file
4. **Select PDF Language**: Choose the language of the uploaded PDF
5. **View Extracted Text**: Preview the extracted text
6. **Choose Target Language**: Select language for conversion
7. **Select Voice**: Choose male or female voice
8. **Convert to Audio**: Click to generate audio file
9. **Play Audio**: Use the built-in audio player
10. **Download MP3**: Save the audio file to your computer

## ⚙️ Configuration

### File Upload
- **Max File Size**: 50MB
- **Accepted Format**: PDF only

### Output Audio
- **Format**: MP3
- **Quality**: Default gTTS quality
- **Storage**: `audio_output/` directory

## 🔧 API Endpoints

### GET `/`
Login page

### GET `/home`
Home/main page

### POST `/api/upload-pdf`
Upload and extract PDF text
- **Parameters**: `pdf_file` (file), `input_language` (string)
- **Returns**: JSON with extracted text and available target languages

### POST `/api/convert-text`
Convert text to audio
- **Parameters**: `text` (string), `target_language` (string), `voice_gender` (string)
- **Returns**: JSON with audio file URL

### GET `/audio/<filename>`
Serve audio file for playback

### GET `/download-audio/<filename>`
Download audio file

## 🐛 Troubleshooting

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
Edit `app.py` and change port:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### PDF Text Extraction Issues
- Ensure PDF is text-based (not scanned image)
- Try uploading a different PDF to test extraction

### Audio Generation Issues
- Check internet connection (required for gTTS)
- Verify text content is present
- Try with shorter text first

## 📱 Browser Compatibility

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📄 File Size Limits

- **Upload PDF**: Max 50MB
- **Generated Audio**: Depends on text length (typically 1-50MB)

## 🔒 Security Notes

- Uploaded files are stored in `uploads/` directory
- Generated audio is stored in `audio_output/` directory
- Files can be manually deleted when no longer needed
- Application uses Flask's built-in security features

## 🚀 Future Enhancements

- [ ] User authentication system
- [ ] File history and saved conversions
- [ ] Advanced language translation options
- [ ] Custom voice settings (accent, speed)
- [ ] Batch PDF processing
- [ ] Cloud storage integration
- [ ] Mobile app version

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the project structure
3. Verify all dependencies are installed
4. Check Flask application logs

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Flask framework
- PyPDF2 for PDF processing
- Google Translate API
- gTTS for text-to-speech conversion
