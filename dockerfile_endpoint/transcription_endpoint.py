from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel
import shutil
import os
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {".wav"}


def allowed_file(filename):
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS

# Nuevo endpoint de healthcheck


@app.get("/healthcheck", tags=["healthcheck"])
async def healthcheck():
    return {"status": "OK"}


@app.post("/v1/transcribe_audio", tags=["v1"], operation_id="transcribe_audio")
async def transcribe_audio(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, detail="Only valid audio files with .wav extension are allowed.")

    # Create a temporary directory to store the uploaded audio file
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    audio_path = os.path.join(temp_dir, file.filename)

    # Save the uploaded audio file
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    start_time = time.time()

    model_size = "small"

    # Run on CPU with FP16
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    # Transcribe audio
    segments, info = model.transcribe(audio_path, beam_size=5)

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

    processing_time = "%d hours, %d minutes, %d seconds" % (
        hours, minutes, seconds)

    # Append processing time to the end of the file
    with open("transcription_result.txt", "a") as f:
        f.write("\nProcessing time: %s" % processing_time)

    # Close the temporary directory and remove the uploaded audio file
    shutil.rmtree(temp_dir)

    # Return the transcription result file
    return FileResponse("transcription_result.txt", media_type="text/plain", filename="transcription_result.txt")
