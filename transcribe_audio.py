from faster_whisper import WhisperModel
import time

start_time = time.time()

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Transcribe audio
segments, info = model.transcribe(
    "./audios_for_testing/audio_test_1.mp3", beam_size=5)

# Print language detection information
print("Detected language '%s' with probability %f" %
      (info.language, info.language_probability))

# Create or open a text file to save the transcription results
with open("transcription_result.txt", "w") as f:
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

end_time = time.time()
processing_time_seconds = end_time - start_time

# Calculate hours, minutes, and remaining seconds
hours = int(processing_time_seconds // 3600)
minutes = int((processing_time_seconds % 3600) // 60)
seconds = int(processing_time_seconds % 60)

print("Processing time: %d hours, %d minutes, %d seconds" %
      (hours, minutes, seconds))

# Append processing time to the end of the file
with open("transcription_result.txt", "a") as f:
    f.write("\nProcessing time: %d hours, %d minutes, %d seconds" %
            (hours, minutes, seconds))

print("Transcription result saved to transcription_result.txt")
