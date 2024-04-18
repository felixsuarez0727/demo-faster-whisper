from flask import Flask, jsonify, request
import base64
import threading
import time

app = Flask(__name__)

# Initially set to 404
queue_status = 404
job_id = "0306133114864968devodifes01.docsis.cox.net1716435646TN0"

# Define a route for the queue endpoint


@app.route('/queue/whisper-queue', methods=['GET'])
def queue():
    global queue_status, job_id

    # Check the current status
    if queue_status == 404:
        # Return a JSON response with a 404 status code and appropriate message
        return jsonify({'error': 'Connection failed'}), 404
    elif queue_status == 200:
        if job_id:
            # Return a JSON response with a 200 status code and the job ID
            return jsonify({'message': 'ID successfully retrieved', 'id': job_id}), 200
        else:
            # Return a JSON response with a 404 status code if job_id is not set
            return jsonify({'message': 'Job ID not found'}), 404

# Define a route for getting job content


@app.route('/job/<requested_job_id>', methods=['GET'])
def get_content(requested_job_id):
    global queue_status, job_id

    # Check if the queue status is 200 and job ID matches the requested_job_id
    if queue_status == 200 and requested_job_id == job_id:
        try:
            # Read the audio file
            audio_file_path = "audio_file_to_64base.wav"
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()

            # Encode the audio data into base64
            base64_audio = base64.b64encode(audio_data).decode("utf-8")

            # Prepare content data
            content_data = {
                'id': job_id,
                'data': base64_audio
            }

            # Return the content data with a 200 status code
            return jsonify(content_data), 200

        except FileNotFoundError:
            # Return a JSON response with a 404 status code if the audio file is not found
            return jsonify({'message': 'Audio file not found'}), 404
        except Exception as e:
            # Return a JSON response with a 500 status code for other exceptions
            return jsonify({'message': 'Internal server error', 'error': str(e)}), 500
    else:
        # Return a JSON response with a 404 status code if job ID is not found or queue status is not 200
        return jsonify({'message': 'Job not found or ID mismatch'}), 404

# Define a route to handle the POST request


@app.route('/job/<requested_job_id>', methods=['POST'])
def post_job(requested_job_id):
    global queue_status, job_id

    if queue_status == 200 and requested_job_id == job_id:
        try:
            # Extract JSON data from the request
            request_data = request.json

            # Extract data from the JSON
            new_job_id = request_data.get('id')
            new_data = request_data.get('data')
            new_output = request_data.get('output')
            new_end = request_data.get('end')

            # Check if required fields are present in the JSON data
            if not new_job_id or not new_data or not new_output or not new_end:
                return jsonify({'message': 'Missing required fields in JSON data'}), 400

            # Update the global job_id with the new job ID
            job_id = new_job_id

            print("\033[92mReceived data:\033[0m")
            print("\033[92mJob ID:\033[0m", new_job_id)
            # print("\033[92mData:\033[0m", new_data)
            print("\033[92mOutput:\033[0m", new_output)
            print("\033[92mEnd:\033[0m", new_end)

            # Return a JSON response indicating success
            return jsonify({'message': 'POST request successful'}), 200

        except Exception as e:
            # Return a JSON response with a 400 status code for any exceptions
            return jsonify({'message': 'Bad request', 'error': str(e)}), 400
    else:
        # Return a JSON response with a 400 status code if queue status is not 200 or job ID mismatch
        return jsonify({'message': 'Invalid request or job ID mismatch'}), 400

# Simulate changing the queue status after a delay


def simulate_status_change():
    global queue_status
    time.sleep(10)  # Wait for 10 seconds
    queue_status = 200  # Change status to 200


if __name__ == '__main__':
    # Start a thread to simulate the status change
    t = threading.Thread(target=simulate_status_change)
    t.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)
