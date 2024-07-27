# OpenAI-Spechify-Your-Docs

OpenAI-Spechify-Your-Docs is a Python project that converts text from `.txt`, `.pdf`, and `.epub` files into speech using OpenAI's Text-to-Speech API. The generated speech is saved as `MP3 files`, with each text file being split into multiple parts if necessary.

## Use Case

Do you have text that you want to listen to in good audio? This tool is ideal for converting emails, articles, or even book-sized texts into MP3 files. For longer texts, the audio is split into manageable parts to ensure a smooth listening experience.

## Features

- Reads text from `.txt`, `.pdf`, and `.epub` files.
- Converts text to speech using OpenAI's Text-to-Speech API.
- Splits long text into multiple parts and saves each part as an MP3 file if the duration exceeds 30 minutes.
- Merges MP3 files into a single audio file, splitting them into multiple parts if necessary.
- Names the MP3 files to indicate the total number of parts.
- Logs progress and errors for easy debugging.

## Installation

### Clone the repository

   ```sh
   git clone https://github.com/Thukyd/OpenAI-Spechify-Your-Docs.git
   cd OpenAI-Spechify-Your-Docs
   ```

### Create and activate a virtual environment (optional but recommended)

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the required dependencies

```sh
pip install -r requirements.txt
```

### Set up your OpenAI API key

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

### Customize the script

- You can change the `max_duration` variable in the script to adjust the maximum duration of each MP3 file.
- You can also decide if you want to keep the intermediate MP3 files by setting the `delete_downloads` variable to `True` or `False`.
- You can choose another OpenAI voice, the default is `shimmer` but there is a range of [alternative voices available](https://platform.openai.com/docs/guides/text-to-speech/quickstart).

## Logging

The script uses logging to provide information about its progress. Logs include messages about the overall process. Errors are also logged for easier debugging. A progress bar is displayed during text-to-speech conversion to track the progress.

## Dependencies

- `requests`
- `PyPDF2`
- `ebooklib`
- `beautifulsoup4`
- `python-dotenv`
- `tqdm` (for displaying a progress bar)
- `pydub` (for audio merging)

Additionally, you need to have `ffmpeg` installed on your system. You can install it using:

- On macOS: `brew install ffmpeg`
- On Ubuntu: `sudo apt-get install ffmpeg`
- On Windows: Download and install from the [FFmpeg website](https://ffmpeg.org/download.html).

## OpenAI Costs and Usage Policies

Please note that using the OpenAI Text-to-Speech API incurs costs. You can find the latest pricing under [Audio Models](https://openai.com/api/pricing/).

Ensure you comply with OpenAI's [usage policies](https://openai.com/policies/usage-policies/). Users of this script should read these policies before running it.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
