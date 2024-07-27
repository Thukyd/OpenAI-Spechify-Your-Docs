import os
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfFileReader
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

def read_text_file(file_path):
    logging.info(f"Reading text file: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(file_path):
    logging.info(f"Reading PDF file: {file_path}")
    pdf = PdfFileReader(file_path)
    text = []
    for page_num in range(pdf.getNumPages()):
        text.append(pdf.getPage(page_num).extractText())
    return "\n".join(text)

def read_epub_file(file_path):
    logging.info(f"Reading ePub file: {file_path}")
    book = epub.read_epub(file_path)
    text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text.append(soup.get_text())
    return "\n".join(text)

def text_to_speech(text, output_file, voice='shimmer'):
    logging.info(f"Converting text to speech: {output_file}")
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
        logging.info(f"Saved {output_file}")
    else:
        logging.error(f"Failed to generate speech: {response.status_code} - {response.text}")

def split_text(text, max_length=3000):
    logging.info("Splitting text into chunks")
    # Split text into chunks of max_length
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def process_file(file_path, voice):
    file_name, file_extension = os.path.splitext(file_path.name)
    output_dir = Path('outputs') / file_name
    if file_extension == '.txt':
        text = read_text_file(file_path)
    elif file_extension == '.pdf':
        text = read_pdf_file(file_path)
    elif file_extension == '.epub':
        text = read_epub_file(file_path)
    else:
        logging.error(f"Unsupported file format: {file_extension}")
        return

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Split text into manageable chunks
    text_chunks = split_text(text)
    total_parts = len(text_chunks)

    # Convert each chunk to speech and save as mp3
    for i, chunk in enumerate(text_chunks):
        output_file = output_dir / f"{file_name}_part{i+1}_of_{total_parts}.mp3"
        text_to_speech(chunk, output_file, voice)

def main():
    # Load OpenAI API key from environment variable
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OpenAI API key is not set. Please check your .env file.")

    # Find the voice you want to use at https://platform.openai.com/docs/guides/text-to-speech/voice-options
    voice = 'shimmer'  # Set the voice to 'shimmer'

    # Process all text, pdf, and epub files in the sources directory
    sources_dir = Path('sources')
    file_paths = list(sources_dir.glob("*.txt")) + list(sources_dir.glob("*.pdf")) + list(sources_dir.glob("*.epub"))
    logging.info(f"Found {len(file_paths)} files to process.")
    for file_path in file_paths:
        logging.info(f"Processing file: {file_path}")
        process_file(file_path, voice)

if __name__ == "__main__":
    main()
