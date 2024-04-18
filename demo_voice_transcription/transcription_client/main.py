import requests
import json
import time
import base64
import numpy as np
import scipy.io.wavfile as wav
import os
import socket
from datetime import datetime, timezone, timedelta

from audio_transcriber import transcribe_audio


# Function to make a GET request to the server
def make_request(url):
    response = requests.get(url)
    return response

# Function to get the IP address of the mock server container
def get_mock_server_ip():
    return 'mock_server'

# Main function to orchestrate the process
def main():
    # Get the IP address of the mock server
    mock_server_ip = get_mock_server_ip()

    # URLs for server communication
    url_get_access = f'http://{mock_server_ip}:8080/queue/whisper-queue'
    url_get_content = f'http://{mock_server_ip}:8080/job/'
    url_post_job = f'http://{mock_server_ip}:8080/job/'

    retries = 3  # Maximum number of retries
    job_id = None  # Variable to store the job ID

    while retries > 0:
        # Attempt to get access from the server
        response = make_request(url_get_access)

        if response.status_code == 404:
            print("\033[91m" + "Connection failed" +
                  "\033[0m" + " Retrying in 5 seconds...")
            time.sleep(5)
            retries -= 1  # Decrement the number of retries
        elif response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print("Response:")
            # Print the response JSON with indentation
            print(json.dumps(data, indent=4))
            job_id = data.get("id")
            if job_id:
                break  # Exit the loop if job ID is successfully retrieved
            else:
                print("\033[91m" + "Error:" + "\033[0m", data.get('message'))
        else:
            # Print the error status code
            print("\033[91m" + "Error:" + "\033[0m", response.status_code)
            break  # Exit the loop if status code is neither 404 nor 200

    if retries == 0:
        print(
            f"Status Code: {response.status_code}, {response.reason}. Exiting.")

    if response.status_code == 200:
        url_get_content = f'{url_get_content}{job_id}'
        content_response = make_request(url_get_content)

        if content_response.status_code == 200:
            # Process the content
            content_data = content_response.json()
            print("Content Data:", content_data)

            audio_data = content_data.get("data")
            if audio_data:
                try:
                    # Pad the base64 encoded string with '=' characters to make its length a multiple of 4
                    padded_data = audio_data + "=" * ((4 - len(audio_data) % 4) % 4)
                    # Decode the base64 data
                    audio_bytes = base64.b64decode(padded_data)
                    # Convert bytes to numpy array
                    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
                    # Set the audio parameters
                    sample_rate = 16000
                    # Save the audio as a WAV file
                    wav.write("audio_file_to_transcribe.wav", sample_rate, audio_np)

                    if os.path.isfile("audio_file_to_transcribe.wav"):
                        print("\033[92mBased64 Audio Converted to \033[0m" +
                              "\033[96maudio_file_to_transcribe.wav\033[0m" + "\033[92m Successfully.\033[0m")

                        # Call the function to transcribe the audio
                        transcription_result = transcribe_audio(
                            "./audio_file_to_transcribe.wav")
                        
                        # Delete the audio file after transcription
                        os.remove("audio_file_to_transcribe.wav")

                    else:
                        print("\033[91m" + "Error:" + "\033[0m" +
                              " Failed to create the audio file.")
                except Exception as e:
                    print("\033[91m" + "Error:" + "\033[0m" +
                          "processing audio data:", e)
            else:
                print("\033[91m" + "Error:" + "\033[0m" +
                      " Audio data not found in content response.")

            # Prepare data to be sent back to the server
            data_to_send = {
                "id": job_id,
                "data": audio_data,
                "output": transcription_result[0] + transcription_result[1],
                "end": datetime.now(timezone(timedelta(hours=-4))).isoformat()
            }

            # Send the data to the server using a POST request
            url_post_job = f'{url_post_job}{job_id}'
            response = requests.post(url_post_job, json=data_to_send)
            if response.status_code == 200:

                print("\033[92mData Sent to\033[0m \033[96m%s\033[0m" %
                      url_post_job)

            else:
                error_message = response.json().get('message', 'Unknown error')
                print("\033[91m" + "Error sending data:" +
                      "\033[0m" + response.status_code, error_message)
        else:
            print("\033[91m" + "Error:" + "\033[0m",
                  content_response.json().get('message'))
    else:
        print("\033[91m" + "Invalid request or job ID mismatch." + "\033[0m")

    time.sleep(4)
    print(data_to_send)


if __name__ == "__main__":
    main()
