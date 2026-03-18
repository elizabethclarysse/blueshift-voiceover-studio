# Video Voice Replacement Tool

A powerful web application that transcribes videos/audio files and replaces the audio with a synthesized voice of your choice.

## Features

- **Multiple File Formats**: Supports MP4, AVI, MOV, MKV, MP3, WAV, M4A, FLAC
- **Drag & Drop Upload**: Easy file upload interface with drag-and-drop support
- **Dual Transcription Methods**:
  - Local Whisper (free, runs on your machine)
  - OpenAI Whisper API (fast, requires API key)
- **Multiple Voice Options**:
  - OpenAI TTS with 6 different voices (alloy, echo, fable, onyx, nova, shimmer)
  - ElevenLabs support (optional)
- **Video Processing**: Automatically replaces audio in videos while preserving video quality
- **Clean UI**: Modern, responsive web interface

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg** (required for audio/video processing)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH

## Installation

1. Clone or navigate to this directory:
```bash
cd voice-replacement-tool
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys (optional but recommended):
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

### API Keys

To use the OpenAI API features, you'll need an OpenAI API key:

1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Generate an API key
3. Add it to `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

For ElevenLabs (optional):
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Get your API key
3. Add to `.env`:
```
ELEVENLABS_API_KEY=your-key-here
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser to:
```
http://localhost:5002
```

3. Upload a video or audio file

4. Choose your options:
   - **Transcription Method**: Local Whisper (free) or OpenAI API (faster)
   - **Voice Method**: OpenAI TTS or ElevenLabs
   - **Voice**: Select from available voices

5. Click "Process Video" and wait for completion

6. Download your processed file

## How It Works

1. **Upload**: File is uploaded and stored temporarily
2. **Extract Audio**: If video, audio is extracted using FFmpeg
3. **Transcribe**: Audio is transcribed using Whisper (local or API)
4. **Synthesize**: Transcription is converted to speech with chosen voice
5. **Replace**: New audio replaces original audio in video
6. **Download**: Processed file is ready for download

## Supported Formats

**Video**: MP4, AVI, MOV, MKV
**Audio**: MP3, WAV, M4A, FLAC

Maximum file size: 500MB

## Available Voices (OpenAI)

- **Alloy**: Neutral, balanced voice
- **Echo**: Clear male voice
- **Fable**: British accent, expressive
- **Onyx**: Deep male voice
- **Nova**: Female, energetic voice
- **Shimmer**: Female, soft voice

## Troubleshooting

**"FFmpeg not found" error:**
- Make sure FFmpeg is installed and in your system PATH
- Test: `ffmpeg -version`

**"Transcription failed" error:**
- For local Whisper: Ensure you have enough RAM (4GB+ recommended)
- For API: Check your OpenAI API key and credits

**Slow processing:**
- Use OpenAI API instead of local Whisper for faster transcription
- Local Whisper can take several minutes for long videos

**Out of memory:**
- Try using a smaller Whisper model (edit app.py line 67: change "base" to "tiny")
- Process shorter videos
- Use the API option instead

## Cost Considerations

**Local Whisper**: Free, but requires computational resources
**OpenAI Whisper API**: $0.006 per minute of audio
**OpenAI TTS**: $15 per 1M characters (~183 hours of audio)
**ElevenLabs**: Varies by plan

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

## File Structure

```
voice-replacement-tool/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary upload storage
├── outputs/              # Processed files
├── temp/                 # Temporary processing files
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Security Notes

- API keys are stored in `.env` (not committed to git)
- Uploaded files are assigned random UUIDs
- Files are stored temporarily and should be cleaned periodically
- Add `.env` to `.gitignore`

## Future Enhancements

- [ ] Batch processing multiple files
- [ ] Progress updates via WebSocket
- [ ] Video preview before download
- [ ] Multiple language support
- [ ] Custom voice cloning (ElevenLabs)
- [ ] Subtitle generation
- [ ] Background noise removal
- [ ] Automatic file cleanup

## License

MIT License - feel free to use and modify

## Support

For issues or questions, please open an issue on the project repository.
