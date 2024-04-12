import os
from faster_whisper import WhisperModel
import time
from tabulate import tabulate

start_time = time.time()

model_size = "small"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Directory containing audio files for testing
audio_folder = "./audios_for_testing"

# List all files in the directory
audio_files = os.listdir(audio_folder)

results = []

# Iterate over each audio file
for audio_file in audio_files:
    file_start_time = time.time()

    # Transcribe audio
    segments, info = model.transcribe(
        os.path.join(audio_folder, audio_file), beam_size=5)

    # Print language detection information
    print("Detected language '%s' with probability %f" %
          (info.language, info.language_probability))

    # Create or open a text file to save the transcription results
    with open("transcription_result.txt", "a", encoding="utf-8") as f:
        # Write language detection information to the file
        f.write("Detected language '%s' with probability %f\n" %
                (info.language, info.language_probability))

        # Write transcription results to the file
        for segment in segments:
            f.write("[%.2fs -> %.2fs] %s\n" %
                    (segment.start, segment.end, segment.text))

            # Print transcription results to console
            print("[%.2fs -> %.2fs] %s" %
                  (segment.start, segment.end, segment.text))

    file_end_time = time.time()
    file_processing_time_seconds = file_end_time - file_start_time

    # Calculate hours, minutes, and remaining seconds
    file_hours = int(file_processing_time_seconds // 3600)
    file_minutes = int((file_processing_time_seconds % 3600) // 60)
    file_seconds = int(file_processing_time_seconds % 60)

    results.append([audio_file, file_hours, file_minutes, file_seconds])

# Print a newline before printing the table
print()

# Print processing time for each file in a table
print(tabulate(results, headers=["Audio File", "Hours", "Minutes", "Seconds"]))


end_time = time.time()
processing_time_seconds = end_time - start_time

# Calculate total processing time
total_hours = int(processing_time_seconds // 3600)
total_minutes = int((processing_time_seconds % 3600) // 60)
total_seconds = int(processing_time_seconds % 60)

print("\nTotal Processing Time: %d hours, %d minutes, %d seconds" %
      (total_hours, total_minutes, total_seconds))

# Append total processing time to the end of the file
with open("transcription_result.txt", "a", encoding="utf-8") as f:
    f.write("\nTotal Processing Time: %d hours, %d minutes, %d seconds" %
            (total_hours, total_minutes, total_seconds))

print("Transcription results saved to transcription_result.txt")
