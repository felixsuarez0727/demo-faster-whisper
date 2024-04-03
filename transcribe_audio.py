from faster_whisper import WhisperModel

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Transcribe audio
segments, info = model.transcribe("./audio_files_for_testing/audio_test_1.mp3", beam_size=5)

# Print language detection information
print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# Create or open a text file to save the transcription results
with open("transcription_result.txt", "w") as f:
    # Write language detection information to the file
    f.write("Detected language '%s' with probability %f\n" % (info.language, info.language_probability))
    
    # Write transcription results to the file
    for segment in segments:
        f.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text))
        
        # Print transcription results to console
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        
print("Transcription result saved to transcription_result.txt")
