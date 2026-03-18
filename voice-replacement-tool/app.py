import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import subprocess
import json
from pathlib import Path
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'mp3', 'wav', 'm4a', 'flac'}

# Create necessary folders
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], 'temp']:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_audio(video_path, audio_output_path):
    """Extract audio from video file using FFmpeg"""
    try:
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # WAV format
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite output
            audio_output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Audio extraction error: {e.stderr.decode()}")
        return False

def transcribe_audio(audio_path, method='whisper'):
    """Transcribe audio using specified method"""
    if method == 'whisper':
        return transcribe_with_whisper(audio_path)
    elif method == 'openai':
        return transcribe_with_openai_api(audio_path)
    elif method == 'google':
        return transcribe_with_google(audio_path)
    else:
        raise ValueError(f"Unknown transcription method: {method}")

def transcribe_with_whisper(audio_path):
    """Transcribe using local Whisper model"""
    try:
        import whisper
        model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
        result = model.transcribe(audio_path)
        return {
            'success': True,
            'text': result['text'],
            'segments': result.get('segments', [])
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def transcribe_with_openai_api(audio_path):
    """Transcribe using OpenAI Whisper API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        with open(audio_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )

        return {
            'success': True,
            'text': transcript.text,
            'segments': getattr(transcript, 'segments', [])
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def transcribe_with_google(audio_path):
    """Transcribe using Google Cloud Speech-to-Text API"""
    try:
        from google.cloud import speech_v1

        client = speech_v1.SpeechClient()

        with open(audio_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech_v1.RecognitionAudio(content=content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)

        # Combine all transcripts
        full_text = ' '.join([result.alternatives[0].transcript
                             for result in response.results])

        return {
            'success': True,
            'text': full_text,
            'segments': []
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def synthesize_speech(text, output_path, voice='alloy', method='openai'):
    """Synthesize speech from text"""
    if method == 'openai':
        return synthesize_with_openai(text, output_path, voice)
    elif method == 'elevenlabs':
        return synthesize_with_elevenlabs(text, output_path, voice)
    elif method == 'google':
        return synthesize_with_google(text, output_path, voice)
    else:
        raise ValueError(f"Unknown synthesis method: {method}")

def synthesize_with_openai(text, output_path, voice='alloy'):
    """Synthesize speech using OpenAI TTS API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Available voices: alloy, echo, fable, onyx, nova, shimmer
        response = client.audio.speech.create(
            model="tts-1",  # or tts-1-hd for higher quality
            voice=voice,
            input=text
        )

        response.stream_to_file(output_path)
        return {'success': True, 'path': output_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def synthesize_with_elevenlabs(text, output_path, voice_id):
    """Synthesize speech using ElevenLabs API"""
    try:
        import requests

        ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return {'success': True, 'path': output_path}
        else:
            return {'success': False, 'error': response.text}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def synthesize_with_google(text, output_path, voice='en-US-Neural2-A'):
    """Synthesize speech using Google Cloud Text-to-Speech API"""
    try:
        from google.cloud import texttospeech_v1

        client = texttospeech_v1.TextToSpeechClient()

        synthesis_input = texttospeech_v1.SynthesisInput(text=text)

        # Parse voice name (format: language-variant or language-variant-gender)
        voice_parts = voice.split('-')
        language_code = f"{voice_parts[0]}-{voice_parts[1]}"

        voice_params = texttospeech_v1.VoiceSelectionParams(
            language_code=language_code,
            name=voice,
        )

        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config
        )

        with open(output_path, 'wb') as out:
            out.write(response.audio_content)

        return {'success': True, 'path': output_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def replace_audio_in_video(video_path, new_audio_path, output_path):
    """Replace audio in video file"""
    try:
        cmd = [
            'ffmpeg', '-i', video_path,
            '-i', new_audio_path,
            '-c:v', 'copy',  # Copy video stream without re-encoding
            '-map', '0:v:0',  # Use video from first input
            '-map', '1:a:0',  # Use audio from second input
            '-shortest',  # Match duration to shortest stream
            '-y',  # Overwrite output
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return {'success': True, 'path': output_path}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': e.stderr.decode()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Generate unique ID for this processing job
    job_id = str(uuid.uuid4())

    # Save uploaded file
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower()
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}.{file_ext}")
    file.save(upload_path)

    return jsonify({
        'success': True,
        'job_id': job_id,
        'filename': filename,
        'file_type': file_ext
    })

@app.route('/process', methods=['POST'])
def process_file():
    data = request.json
    job_id = data.get('job_id')
    transcription_method = data.get('transcription_method', 'whisper')
    voice_method = data.get('voice_method', 'openai')
    voice = data.get('voice', 'alloy')

    if not job_id:
        return jsonify({'error': 'No job_id provided'}), 400

    # Find uploaded file
    upload_files = list(Path(app.config['UPLOAD_FOLDER']).glob(f"{job_id}.*"))
    if not upload_files:
        return jsonify({'error': 'File not found'}), 404

    upload_path = str(upload_files[0])
    file_ext = upload_path.rsplit('.', 1)[1].lower()

    # Define paths
    temp_audio = f"temp/{job_id}_extracted.wav"
    new_audio = f"temp/{job_id}_synthesized.mp3"
    output_file = f"{job_id}_output.{file_ext}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file)

    try:
        # Step 1: Extract audio from video
        if file_ext in ['mp4', 'avi', 'mov', 'mkv']:
            print(f"Extracting audio from video...")
            if not extract_audio(upload_path, temp_audio):
                return jsonify({'error': 'Failed to extract audio'}), 500
        else:
            # If it's already an audio file, use it directly
            temp_audio = upload_path

        # Step 2: Transcribe audio
        print(f"Transcribing audio using {transcription_method}...")
        transcription = transcribe_audio(temp_audio, method=transcription_method)

        if not transcription.get('success'):
            return jsonify({'error': f"Transcription failed: {transcription.get('error')}"}), 500

        # Step 3: Synthesize new audio
        print(f"Synthesizing speech using {voice_method} with voice {voice}...")
        synthesis = synthesize_speech(
            transcription['text'],
            new_audio,
            voice=voice,
            method=voice_method
        )

        if not synthesis.get('success'):
            return jsonify({'error': f"Speech synthesis failed: {synthesis.get('error')}"}), 500

        # Step 4: Replace audio in video (or just return new audio if input was audio)
        if file_ext in ['mp4', 'avi', 'mov', 'mkv']:
            print(f"Replacing audio in video...")
            result = replace_audio_in_video(upload_path, new_audio, output_path)

            if not result.get('success'):
                return jsonify({'error': f"Audio replacement failed: {result.get('error')}"}), 500
        else:
            # For audio files, just return the synthesized audio
            import shutil
            shutil.copy(new_audio, output_path)

        return jsonify({
            'success': True,
            'job_id': job_id,
            'transcription': transcription['text'],
            'output_file': output_file,
            'download_url': url_for('download_file', filename=output_file)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/voices')
def get_voices():
    """Return available voices for different services"""
    voices = {
        'openai': [
            {'id': 'alloy', 'name': 'Alloy', 'description': 'Neutral, balanced'},
            {'id': 'echo', 'name': 'Echo', 'description': 'Male, clear'},
            {'id': 'fable', 'name': 'Fable', 'description': 'British accent, expressive'},
            {'id': 'onyx', 'name': 'Onyx', 'description': 'Deep male'},
            {'id': 'nova', 'name': 'Nova', 'description': 'Female, energetic'},
            {'id': 'shimmer', 'name': 'Shimmer', 'description': 'Female, soft'}
        ]
    }

    # Add ElevenLabs voices if API key is configured
    if os.getenv('ELEVENLABS_API_KEY'):
        # You can fetch voices from ElevenLabs API here
        pass

    return jsonify(voices)

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'ffmpeg_available': os.system('which ffmpeg') == 0
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
