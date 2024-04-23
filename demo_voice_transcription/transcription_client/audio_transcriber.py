from faster_whisper import WhisperModel
import time
from typing import Tuple
import multiprocessing

# Determine the number of CPU cores available
cpu_count = multiprocessing.cpu_count()

# Load the model once from local folder
model = WhisperModel("small", device="cpu", num_workers=4, cpu_threads=min(8, cpu_count))


def transcribe_audio(audio_file_path: str) -> Tuple[str, str, str]:
    print("\033[92m" + "Transcription Starting..." + "\033[0m")

    try:
        start_time = time.time()

        # Transcribe audio
        result = model.transcribe(audio_file_path, language="en")
        
        # Extract segments from the generator object
        segments = list(result[0])

        language_info = result[1].language  # Extract language information
        if language_info:
            print("\033[92mDetected language:", language_info, "\033[0m")
        else:
            print("\033[91mNo language information found in the result\033[0m")

        # Prepare transcribed text
        transcribed_text = " ".join(segment.text for segment in segments)

        end_time = time.time()
        processing_time_seconds = end_time - start_time

        # Calculate hours, minutes, and remaining seconds
        hours = int(processing_time_seconds // 3600)
        minutes = int((processing_time_seconds % 3600) // 60)
        seconds = int(processing_time_seconds % 60)

        processing_time_str = "Processing time: %d hours, %d minutes, %d seconds" % (
            hours, minutes, seconds)

        print("\033[92m" + "Transcription Ended Successfully" + "\033[0m")

        return transcribed_text, processing_time_str, language_info

    except Exception as e:
        # Handle any exceptions gracefully
        print("An error occurred:", e)
        return "", "Error occurred during transcription", "Unknown"


