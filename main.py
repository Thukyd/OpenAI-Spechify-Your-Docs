import os  # .env files
from dotenv import load_dotenv  # For loading environment variables from .env file
import requests  # the OpenAI python library does not support the TTS API, so I use requests
from PyPDF2 import PdfFileReader  
from ebooklib import epub  
from bs4 import BeautifulSoup  # For parsing HTML content from EPUB files
from pathlib import Path  
import logging  
from tqdm import tqdm  # progress bar
from pydub import AudioSegment  # For handling audio files merging (less single mp3 files)
import shutil  # For deleting directories

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Initialize consumption statistics
api_calls = 0
total_duration_ms = 0
total_characters = 0
final_mp3_count = 0

def read_text_file(file_path):
    """Reads text from a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(file_path):
    """Reads text from a .pdf file."""
    pdf = PdfFileReader(file_path)
    text = []
    for page_num in range(pdf.getNumPages()):
        text.append(pdf.getPage(page_num).extractText())
    return "\n".join(text)

def read_epub_file(file_path):
    """Reads text from an .epub file."""
    book = epub.read_epub(file_path)
    text = []
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text.append(soup.get_text(strip=True))
    return "\n".join(text)

def text_to_speech(text, output_file, voice='shimmer'):
    """Converts text to speech using OpenAI's API and saves as MP3."""
    global api_calls, total_duration_ms

    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-1",
        "input": text,
        "voice": voice
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        audio = AudioSegment.from_mp3(output_file)
        total_duration_ms += len(audio)
        api_calls += 1
    else:
        logging.error(f"Failed to generate speech: {response.status_code} - {response.text}")

def split_text(text, max_length=3000):
    """Splits text into smaller chunks."""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def merge_mp3_files(download_dir, output_dir, file_name, max_duration_minutes=30):
    """Merges MP3 files into parts with a maximum duration."""
    global final_mp3_count

    max_duration = max_duration_minutes * 60 * 1000  # convert minutes to milliseconds
    audio_files = sorted(download_dir.glob(f"{file_name}_*.mp3"))
    combined = AudioSegment.empty()
    part_number = 1
    merged_files = []
    zero_padding = len(str(len(audio_files)))

    for file in tqdm(audio_files, desc="Merging files", unit="file"):
        audio = AudioSegment.from_mp3(file)
        logging.info(f"Processing file: {file}, duration: {len(audio)}ms")
        if len(combined) + len(audio) > max_duration:
            merged_file = output_dir / f"{file_name}_{str(part_number).zfill(zero_padding)}_of_{str(len(audio_files)).zfill(zero_padding)}.mp3"
            combined.export(merged_file, format="mp3").close()
            logging.info(f"Merged file created: {merged_file}")
            merged_files.append(merged_file)
            combined = AudioSegment.empty()
            part_number += 1
        combined += audio

    if len(combined) > 0:
        merged_file = output_dir / f"{file_name}_{str(part_number).zfill(zero_padding)}_of_{str(len(audio_files)).zfill(zero_padding)}.mp3"
        combined.export(merged_file, format="mp3").close()
        logging.info(f"Merged file created: {merged_file}")
        merged_files.append(merged_file)

    final_mp3_count += len(merged_files)
    return len(merged_files)

def process_file(file_path, voice, max_duration_minutes=30, delete_downloads=True):
    """Processes a file to convert its content to speech."""
    global total_characters

    file_name, file_extension = os.path.splitext(file_path.name)
    output_dir = Path('outputs') / file_name
    download_dir = Path('downloads') / file_name

    if file_extension == '.txt':
        text = read_text_file(file_path)
    elif file_extension == '.pdf':
        text = read_pdf_file(file_path)
    elif file_extension == '.epub':
        text = read_epub_file(file_path)
    else:
        logging.error(f"Unsupported file format: {file_extension}")
        return

    if not text.strip():
        logging.warning(f"No text extracted from {file_path}")
        return

    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    text_chunks = split_text(text)
    total_parts = len(text_chunks)
    zero_padding = len(str(total_parts))

    for i, chunk in enumerate(tqdm(text_chunks, desc=f"Processing {file_name}", unit="chunk")):
        output_file = download_dir / f"{file_name}_{str(i + 1).zfill(zero_padding)}_of_{str(total_parts).zfill(zero_padding)}.mp3"
        if not output_file.exists():
            total_characters += len(chunk)
            text_to_speech(chunk, output_file)
        else:
            logging.info(f"Chunk {i + 1}/{total_parts} already exists as {output_file}")

    all_parts_exist = all(
        (download_dir / f"{file_name}_{str(i + 1).zfill(zero_padding)}_of_{str(total_parts).zfill(zero_padding)}.mp3").exists()
        for i in range(total_parts)
    )

    if all_parts_exist:
        merge_mp3_files(download_dir, output_dir, file_name, max_duration_minutes)
        
    if delete_downloads:
        shutil.rmtree(download_dir)
        logging.info(f"Deleted download directory: {download_dir}")

def main(delete_downloads=True, voice='shimmer', max_duration_minutes=30):
    """
    Main function to process all text, pdf, and epub files in the 'sources' directory.

    Parameters:
    - delete_downloads (bool): 
        The script downloads the mp3 files to the 'downloads' directory before merging them.
        The orginal mp3 files are small chunks of the text. The merged mp3 files are the final output.
        This parameter specifies whether to delete the chunked mp3 files from openAI after processing. 
        Default is True.

    - voice (str): 
        The voice to use for speech synthesis. 
        See more voices at https://platform.openai.com/docs/guides/text-to-speech/quickstart
        Default is 'shimmer'.

    - max_duration_minutes (int):
        The chunked mp3 files are merged into a single mp3 file with a maximum duration.
        If the total duration of the chunked mp3 files exceeds this value, they are split into multiple parts.
        Default is 30 min.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please check your .env file.")

    sources_dir = Path('sources')
    file_paths = list(sources_dir.glob("*.txt")) + list(sources_dir.glob("*.pdf")) + list(sources_dir.glob("*.epub"))
    logging.info(f"Found {len(file_paths)} files to process.")

    for file_path in file_paths:
        logging.info(f"Processing file: {file_path}")
        process_file(file_path, voice, max_duration_minutes, delete_downloads)
    
    # Print the consumption statistics
    logging.info(f"Total API calls made: {api_calls}")
    logging.info(f"Total audio duration generated: {total_duration_ms / 1000 / 60:.2f} minutes")
    logging.info(f"Total characters processed: {total_characters}")
    logging.info(f"Total final MP3 files: {final_mp3_count}")

if __name__ == "__main__":
    main()
