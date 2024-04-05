# 🤖 Whisper Transcription

This Python script utilizes the [faster-whisper](https://github.com/SYSTRAN/faster-whisper) package for transcribing audio files using the Whisper model. The faster-whisper package is a reimplementation of OpenAI's Whisper model using CTranslate2.[OpenAI's Whisper model](https://github.com/openai/whisper) is an advanced implementation of Automatic Speech Recognition (ASR). It employs modern deep learning techniques to accurately transcribe human speech into text. Whisper has been trained on a large amount of high-quality audio data, enabling it to recognize a wide range of dialects and accents. Its accuracy and speed make it ideal for real-time transcription applications.

## 🛠️Prerequisites

- Python 3.8 or higher
- Docker (optional)

## 🚀 Using Python Script

1. **Set Up a Virtual Environment:**

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows, use `venv\Scripts\activate`
```

2. Install the necessary Python dependencies:

```bash
pip install faster-whisper
```

3. Run the Python script `transcribe_audio.py`. Make sure to replace `audio_files_for_testing/audio_test_1.mp3` with the path to your audio file if necessary:

```bash
python transcribe_audio.py
```

This will transcribe the audio file specified, print on console and save the results to a text file named `transcription_result.txt`.

<img src="./imgs/transcription_result.png"/>

## 🐳 Using DockerFile for the script

1. Build the Docker image inside the `dockerfile_script` folder:

```bash
docker build -t whisper_transcription_container .
```

2. Execute the python container from outside it

```bash
docker run whisper_transcription_container
```

<img src="./imgs/run_docker_outside_container.png"/>

or

3. Get into the docker container:

```bash
docker run -it --rm whisper_transcription_container bash
```

3. Execute the python script inside the container

```bash
python transcribe_audio.py
```

This will execute the Python script inside the Docker container, transcribe the audio file, and save the results to `transcription_result.txt`.

<img src="./imgs/docker_transcription_result.png"/>

## ℹ️ Additional Notes

- Ensure that the audio file path specified in the script is correct and accessible.
- The Docker image can be used to run the transcription in an isolated environment without worrying about dependencies.

## 🧑🏻‍💻 Using the Fast API Endpoint

1. Set Up a Virtual Environment:

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows, use `venv\Scripts\activate`
```

2. Install Dependencies:

```bash
pip install -r requirements.txt
```

3. Run the FastAPI Application:

```bash
uvicorn transcription_endpoint:app --reload
```

This will start the FastAPI application, and you can access the endpoint at `http://127.0.0.1:8000/docs#/default/transcribe_audio_transcribe_audio__post`.

4. **Results**

<img src="./imgs/endpoint_results.png"/>

## 🌐🌏 Using the DockerFile for the FastAPI Endpoint:

1. Build the Docker image inside the `dockerfile_endpoint` folder:

```bash
cd dockerfile_endpoint
docker build -t dockerfile_endpoint .
```

<img src="./imgs/build_dockerfile_endpoint.png"/>

2. Run the Docker Container:

```bash
docker run -p 80:8000 dockerfile_endpoint
```

<img src="./imgs/build_dockerfile_endpoint.png"/>

This will start the FastAPI application, and you can access the endpoint at `http://localhost/docs#/default/transcribe_audio_transcribe_audio__post`.

4. **Results**

<img src="./imgs/docker_endpoint_results.png"/>
