# OpenAI-Spechify-Your-Docs

OpenAI-Spechify-Your-Docs is a Python project that converts text from `.txt`, `.pdf`, and `.epub` files into speech using OpenAI's Text-to-Speech API. The generated speech is saved as MP3 files, with each text file being split into multiple parts if necessary.

## Features

- Reads text from `.txt`, `.pdf`, and `.epub` files.
- Converts text to speech using OpenAI's Text-to-Speech API.
- Splits long text into multiple parts and saves each part as an MP3 file.
- Names the MP3 files to indicate the total number of parts.
- Logs progress and errors for easy debugging.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Thukyd/OpenAI-Spechify-Your-Docs.git
   cd OpenAI-Spechify-Your-Docs

Sure, here's the text you provided formatted as Markdown:

```markdown
## Create and activate a virtual environment (optional but recommended):

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Install the required dependencies

```sh
pip install -r requirements.txt
```

## Set up your OpenAI API key

Create a `.env` file in the project root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Place your text files in the `sources` directory

Ensure your `.txt`, `.pdf`, and `.epub` files are in the `sources` directory.

### Run the script

```sh
python main.py
```

### Check the `outputs` directory for the generated MP3 files

The MP3 files will be saved in subdirectories named after the original text files, with filenames indicating the total number of parts.

## Logging

The script uses logging to provide information about its progress. Logs include messages about file reading, text splitting, text-to-speech conversion, and saving files. Errors are also logged for easier debugging.

## Dependencies

- `requests`
- `PyPDF2`
- `ebooklib`
- `beautifulsoup4`
- `python-dotenv`

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to OpenAI for providing the API for text-to-speech conversion.
- Inspired by the need to easily convert documents to audio format for accessibility and convenience.
