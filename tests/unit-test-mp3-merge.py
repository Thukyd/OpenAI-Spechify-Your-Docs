import os
from pathlib import Path
import unittest
from pydub import AudioSegment
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def merge_mp3_files(output_dir, file_name, max_duration_minutes=2):
    """Merges MP3 files into parts with a maximum duration."""
    max_duration = max_duration_minutes * 60 * 1000  # convert minutes to milliseconds
    audio_files = sorted(output_dir.glob(f"{file_name}_part*.mp3"))
    combined = AudioSegment.empty()
    part_number = 1
    merged_files = []

    for file in audio_files:
        audio = AudioSegment.from_mp3(file)
        logging.info(f"Processing file: {file}, duration: {len(audio)}ms")
        if len(combined) + len(audio) > max_duration:
            merged_file = output_dir / f"{file_name}_merged_part{part_number}.mp3"
            combined.export(merged_file, format="mp3").close()
            logging.info(f"Merged file created: {merged_file}")
            merged_files.append(merged_file)
            combined = AudioSegment.empty()
            part_number += 1
        combined += audio

    if len(combined) > 0:
        merged_file = output_dir / f"{file_name}_merged_part{part_number}.mp3"
        combined.export(merged_file, format="mp3").close()
        logging.info(f"Merged file created: {merged_file}")
        merged_files.append(merged_file)

    return len(merged_files)

class TestMP3Merge(unittest.TestCase):

    def setUp(self):
        self.output_dir = Path('tests/outputs/test_merge')
        self.file_name = 'test_audio'
        os.makedirs(self.output_dir, exist_ok=True)

    def create_test_files(self):
        """Creates test MP3 files."""
        silent_segment = AudioSegment.silent(duration=60000)  # 1 minute silent audio
        for i in range(5):
            part_file = self.output_dir / f"{self.file_name}_part{i + 1}_of_5.mp3"
            silent_segment.export(part_file, format="mp3").close()
            logging.info(f"Created test file: {part_file}")

    def test_merge_mp3_files(self):
        self.create_test_files()
        merged_count = merge_mp3_files(self.output_dir, self.file_name, max_duration_minutes=2)
        self.assertEqual(merged_count, 3)  # Expect 3 merged files (2 min max duration each)

        # Check if merged files exist
        for i in range(1, merged_count + 1):
            merged_file = self.output_dir / f"{self.file_name}_merged_part{i}.mp3"
            self.assertTrue(merged_file.exists())
            logging.info(f"Verified merged file exists: {merged_file}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
