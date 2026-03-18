from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import PyPDF2

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

try:
    from googletrans import Translator
except ImportError:
    Translator = None

try:
    import docx
except ImportError:
    docx = None

try:
    from ebooklib import epub
    from ebooklib import ITEM_DOCUMENT
    from bs4 import BeautifulSoup
except ImportError:
    epub = None
    ITEM_DOCUMENT = None
    BeautifulSoup = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_OUTPUT_FOLDER'] = os.path.join('static', 'audio')
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024  # 80MB
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'epub'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_OUTPUT_FOLDER'], exist_ok=True)

LANGUAGE_CODES = {
    'English': 'en',
    'Tamil': 'ta',
    'Hindi': 'hi',
    'Malayalam': 'ml',
    'Telugu': 'te',
    'Spanish': 'es',
    'Chinese': 'zh-cn'
}
LANGUAGE_CONVERSION = {
    'English': ['Tamil', 'Hindi', 'Malayalam', 'Telugu', 'Spanish', 'Chinese'],
    'Tamil': ['English', 'Hindi', 'Malayalam', 'Telugu', 'Spanish', 'Chinese'],
    'Hindi': ['English', 'Tamil', 'Malayalam', 'Telugu', 'Spanish', 'Chinese'],
    'Malayalam': ['English', 'Tamil', 'Hindi', 'Telugu', 'Spanish', 'Chinese'],
    'Telugu': ['English', 'Tamil', 'Hindi', 'Malayalam', 'Spanish', 'Chinese'],
    'Spanish': ['English', 'Tamil', 'Hindi', 'Malayalam', 'Telugu', 'Chinese'],
    'Chinese': ['English', 'Tamil', 'Hindi', 'Malayalam', 'Telugu', 'Spanish']
}
translator = Translator() if Translator else None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()
    except Exception as e:
        app.logger.error(f"TXT extraction error: {e}")
        return None


def extract_text_from_docx(file_path):
    if docx is None:
        app.logger.error("python-docx not installed")
        return None
    try:
        document = docx.Document(file_path)
        parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n".join(parts).strip()
    except Exception as e:
        app.logger.error(f"DOCX extraction error: {e}")
        return None


def extract_text_from_epub(file_path):
    if epub is None or BeautifulSoup is None:
        app.logger.error("ebooklib or beautifulsoup4 not installed")
        return None
    try:
        book = epub.read_epub(file_path)
        parts = []
        for item in book.get_items_of_type(ITEM_DOCUMENT):
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            if text:
                parts.append(text)
        return "\n".join(parts).strip()
    except Exception as e:
        app.logger.error(f"EPUB extraction error: {e}")
        return None


def extract_text_from_pdf(file_path):
    try:
        text_parts = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = ''
                try:
                    page_text = page.extract_text() or ''
                except Exception:
                    page_text = ''
                if page_text:
                    text_parts.append(page_text)
        extracted = "\n".join(text_parts).strip()
        if extracted:
            app.logger.info(f"Extracted {len(extracted.split())} words from PDF")
            return extracted
        app.logger.warning("PDF extraction returned no text")
        return None
    except Exception as e:
        app.logger.error(f"PDF extraction error: {e}")
        return None


def translate_text(text, target_language='English'):
    if not text or not isinstance(text, str) or not text.strip():
        return text
    if translator is None:
        app.logger.warning("googletrans not installed; skipping translation")
        return text
    target_code = LANGUAGE_CODES.get(target_language, 'en')
    try:
        translated = translator.translate(text, dest=target_code)
        return translated.text
    except Exception as e:
        app.logger.warning(f"Translation error: {e}")
        return text


def chunk_text(text, chunk_size=500):
    words = text.split()
    if not words:
        return []
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def extract_words_with_timing(text, audio_duration):
    try:
        words = text.split()
        if not words or audio_duration <= 0:
            return []
        avg = audio_duration / len(words)
        timings = []
        current = 0.0
        for i, w in enumerate(words):
            timings.append({'word': w, 'start': round(current, 2), 'end': round(current + avg, 2), 'index': i})
            current += avg
        return timings
    except Exception as e:
        app.logger.error(f"Word timing error: {e}")
        return []


def merge_audio_chunks(chunk_paths, output_path):
    if AudioSegment is None:
        app.logger.warning("pydub not installed; cannot merge chunks")
        return False
    try:
        combined = AudioSegment.empty()
        for p in chunk_paths:
            combined += AudioSegment.from_file(p, format='mp3')
        combined.export(output_path, format='mp3')
        return True
    except Exception as e:
        app.logger.warning(f"Audio merge failed: {e}")
        return False


def generate_audio_local_pyttsx3(text, output_path):
    if pyttsx3 is None:
        app.logger.warning("pyttsx3 not installed for fallback")
        return False
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return os.path.exists(output_path)
    except Exception as e:
        app.logger.error(f"pyttsx3 fallback failed: {e}")
        return False


def generate_audio(text, language='English', voice_gender='Female', chunk_size=400):
    if gTTS is None:
        app.logger.error("gTTS not installed")
        return None
    if not text or not isinstance(text, str) or not text.strip():
        app.logger.error("No valid text for audio generation")
        return None

    safe_text = text.strip()
    if len(safe_text) > 5000:
        app.logger.info(f"Truncating text from {len(safe_text)} to 5000 chars")
        safe_text = safe_text[:5000]

    chunks = chunk_text(safe_text, chunk_size=chunk_size)
    if not chunks:
        app.logger.error("No chunks generated from text")
        return None

    output_filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(app.config['AUDIO_OUTPUT_FOLDER'], output_filename)
    if not os.path.isdir(app.config['AUDIO_OUTPUT_FOLDER']):
        os.makedirs(app.config['AUDIO_OUTPUT_FOLDER'], exist_ok=True)

    def save_gtts_chunk(text_chunk, target_path):
        retries = 2
        last_error = None
        for attempt in range(1, retries + 1):
            try:
                tts = gTTS(text=text_chunk, lang=LANGUAGE_CODES.get(language, 'en'), slow=False)
                tts.save(target_path)
                return True
            except Exception as e:
                last_error = e
                app.logger.warning(f"gTTS attempt {attempt} failed: {e}")
        app.logger.error(f"gTTS failed after {retries} attempts: {last_error}")
        return False

    temp_files = []
    try:
        if len(chunks) == 1:
            if not save_gtts_chunk(chunks[0], output_path):
                app.logger.warning("gTTS failed for single chunk; trying pyttsx3 fallback")
                if not generate_audio_local_pyttsx3(safe_text, output_path):
                    return None
        else:
            for idx, chunk in enumerate(chunks):
                temp_path = os.path.join(app.config['AUDIO_OUTPUT_FOLDER'], f"{uuid.uuid4()}_{idx}.mp3")
                if not save_gtts_chunk(chunk, temp_path):
                    raise RuntimeError("Chunk audio generation failed")
                temp_files.append(temp_path)

            if not merge_audio_chunks(temp_files, output_path):
                app.logger.warning("Chunk merge failed, retrying single generation")
                if not save_gtts_chunk(safe_text, output_path):
                    app.logger.warning("gTTS single fallback failed; trying pyttsx3")
                    if not generate_audio_local_pyttsx3(safe_text, output_path):
                        raise RuntimeError("Audio fallback failed")
    except Exception as e:
        app.logger.error(f"Audio generation failed: {e}")
        for p in temp_files:
            try:
                os.remove(p)
            except Exception:
                pass
        if os.path.exists(output_path):
            os.remove(output_path)
        return None
    finally:
        for p in temp_files:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass

    duration = max(1.0, len(safe_text.split()) / 2.5)
    return {'filename': output_filename, 'duration': duration, 'word_timings': extract_words_with_timing(safe_text, duration)}


def extract_text_page_by_page(file_path, max_pages=None):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            pages = []
            for idx, page in enumerate(reader.pages):
                if max_pages and idx >= max_pages:
                    break
                page_text = ''
                try:
                    page_text = page.extract_text() or ''
                except Exception:
                    page_text = ''
                pages.append({'page_number': idx + 1, 'text': page_text, 'word_count': len(page_text.split())})
        return pages, len(pages)
    except Exception as e:
        app.logger.error(f"Page extraction failed: {e}")
        return None, 0


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/audio/<path:filename>')
def serve_audio(filename):
    audio_path = os.path.join(app.config['AUDIO_OUTPUT_FOLDER'], filename)
    if not os.path.exists(audio_path):
        return jsonify({'success': False, 'error': 'Audio file not found'}), 404
    return send_file(audio_path, mimetype='audio/mpeg')


@app.route('/download-audio/<path:filename>')
def download_audio(filename):
    audio_path = os.path.join(app.config['AUDIO_OUTPUT_FOLDER'], filename)
    if not os.path.exists(audio_path):
        return jsonify({'success': False, 'error': 'Audio file not found'}), 404
    return send_file(audio_path, mimetype='audio/mpeg', as_attachment=True, download_name=filename)


@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['pdf_file']
        if not file or file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF/TXT/DOCX/EPUB files are allowed'}), 400

        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        ext = get_file_extension(file.filename)
        extracted_text = None
        if ext == 'pdf':
            extracted_text = extract_text_from_pdf(file_path)
        elif ext == 'txt':
            extracted_text = extract_text_from_txt(file_path)
        elif ext == 'docx':
            extracted_text = extract_text_from_docx(file_path)
        elif ext == 'epub':
            extracted_text = extract_text_from_epub(file_path)

        if not extracted_text:
            return jsonify({'error': f'Failed to extract text from {ext.upper()}'}), 400

        input_language = request.form.get('input_language', 'English')
        return jsonify({'success': True, 'extracted_text': extracted_text, 'input_language': input_language, 'target_languages': LANGUAGE_CONVERSION.get(input_language, ['English', 'Hindi', 'Malayalam']), 'file_path': file_path})
    except Exception as e:
        app.logger.error(f"Upload error: {e}")
        return jsonify({'error': 'Server error occurred'}), 500


@app.route('/api/translate-text', methods=['POST'])
def translate_text_endpoint():
    try:
        data = request.json or {}
        text = data.get('text', '')
        target_lang = data.get('target_language', 'English')
        if not text or not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        translated = translate_text(text, target_lang)
        return jsonify({'success': True, 'translated_text': translated, 'language': target_lang})
    except Exception as e:
        app.logger.error(f"Translate endpoint error: {e}")
        return jsonify({'error': 'Server error occurred'}), 500


@app.route('/api/get-pdf-pages', methods=['POST'])
def get_pdf_pages():
    try:
        data = request.json or {}
        file_path = data.get('file_path', '')
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 400
        pages, total_pages = extract_text_page_by_page(file_path)
        if pages is None:
            return jsonify({'error': 'Failed to extract pages'}), 500
        return jsonify({'success': True, 'pages': pages, 'total_pages': total_pages})
    except Exception as e:
        app.logger.error(f"Get PDF pages error: {e}")
        return jsonify({'error': 'Server error occurred'}), 500


@app.route('/api/get-word-timings', methods=['POST'])
def get_word_timings():
    try:
        data = request.json or {}
        text = data.get('text', '')
        duration = float(data.get('duration', 0) or 0)
        if not text or not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        timings = extract_words_with_timing(text, duration)
        return jsonify({'success': True, 'word_timings': timings, 'total_words': len(text.split()), 'duration': duration})
    except Exception as e:
        app.logger.error(f"Word timings error: {e}")
        return jsonify({'error': 'Server error occurred'}), 500


@app.route('/api/convert-text', methods=['POST'])
def convert_text():
    try:
        print("STEP 1: Request received")
        data = request.json or {}
        text = data.get('text', '')
        target_language = data.get('target_language', 'English')
        voice_gender = data.get('voice_gender', 'Female')

        if not text or not isinstance(text, str) or not text.strip():
            print("ERROR: Empty text")
            return jsonify({'success': False, 'error': 'No text provided'}), 400

        print("STEP 2: Text length", len(text))

        translated = translate_text(text, target_language)
        print("STEP 3: Translation done")

        if len(translated) > 5000:
            translated = translated[:5000]

        audio_data = generate_audio(translated, language=target_language, voice_gender=voice_gender, chunk_size=700)
        if not audio_data:
            print("ERROR: Audio generation failed")
            return jsonify({'success': False, 'error': 'Failed to generate audio'}), 500

        print("STEP 4: Audio generated")
        audio_url = f"/static/audio/{audio_data['filename']}"
        app.logger.info(f"Audio saved at: {os.path.join(app.config['AUDIO_OUTPUT_FOLDER'], audio_data['filename'])}")
        return jsonify({'success': True, 'audio_url': audio_url, 'audio_filename': audio_data['filename'], 'translated_text': translated, 'duration': audio_data['duration'], 'word_timings': audio_data['word_timings']})
    except Exception as e:
        app.logger.error(f"Convert text error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
