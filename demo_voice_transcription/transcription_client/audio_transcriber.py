from faster_whisper import WhisperModel
import time
from typing import Tuple


def transcribe_audio(audio_file_path: str) -> Tuple[str, str]:
    print("\033[92m" + "Transcription Starting..." + "\033[0m")

    """
    Transcribes audio from the given file path.

    Args:
    audio_file_path (str): Path to the audio file.

    Returns:
    Tuple[str, str]: A tuple containing the transcribed text and processing time string.
    """
    try:
        start_time = time.time()

        model_size = "small"

        # Run on CPU with INT8
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

        # Transcribe audio
        segments, info = model.transcribe(audio_file_path, beam_size=5)

        # Prepare transcribed text
        transcribed_text = " ".join([segment.text for segment in segments])

        # Print language detection information
        print("\033[92mDetected language: %s\033[0m" % info.language)

        end_time = time.time()
        processing_time_seconds = end_time - start_time

        # Calculate hours, minutes, and remaining seconds
        hours = int(processing_time_seconds // 3600)
        minutes = int((processing_time_seconds % 3600) // 60)
        seconds = int(processing_time_seconds % 60)

        processing_time_str = "Processing time: %d hours, %d minutes, %d seconds" % (
            hours, minutes, seconds)

        print("\033[92m" + "Transcription Ended Sucessfully" + "\033[0m")

        return transcribed_text, processing_time_str

    except Exception as e:
        # Handle any exceptions gracefully
        print("An error occurred:", e)
        return "", "Error occurred during transcription"
