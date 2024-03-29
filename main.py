import os
import json
import boto3
import requests
import time

from dotenv import load_dotenv
load_dotenv()

# Get environment variables
job_queue_url = os.getenv('JOB_QUEUE_URL')
result_queue_url = os.getenv('RESULT_QUEUE_URL')
api_key = os.getenv('API_KEY')

# Initialize a session using Amazon SQS
sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION'))

def get_payload_config(stop):
    return {
        "stream": False,
        "n_predict": 400,
        "temperature": 1.31,
        "stop": [
            stop,
        ],
        "repeat_last_n": 256,
        "repeat_penalty": 1.17,
        "top_k": 49,
        "top_p": 0.14,
        "tfs_z": 1,
        "typical_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "mirostat": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "grammar": "",
        "n_probs": 0,
        "prompt": ""
    }

def run_inference(message_data):
    # Parse the message body to get the 'stop' and 'prompt' values
    stop = message_data.get('stop')
    prompt = message_data.get('prompt')

    # Define the URL
    url = f"{os.getenv('COMPLETION_URL')}/completion"

    # Get the payload configuration and update the prompt field
    payload = get_payload_config(stop)
    payload['prompt'] = prompt

    # Send the POST request
    response = requests.post(url, headers={'Content-Type': 'application/json',
                                           'Authorization': f'Bearer {os.getenv("API_KEY")}'}, json=payload)

    # Ensure the request was successful
    response.raise_for_status()

    # Return the response data
    return response.json()


def process_messages():
    while True:
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=job_queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        if 'Messages' in response:
            for message in response['Messages']:
                # Verify API key (assuming it's part of the message body)
                message_body = json.loads(message['Body'])
                if 'api_key' not in message_body or message_body['api_key'] != api_key:
                    print('Invalid API key')
                    continue  # Skip processing if the API key is invalid

                # Run inference
                inference_result = run_inference(message_body)

                result_message = {
                    'incoming_message': message_body,
                    'inference_result': inference_result
                }

                # Send inference result to the result queue
                sqs.send_message(
                    QueueUrl=result_queue_url,
                    MessageBody=json.dumps(result_message)
                )

                # Delete received message from queue
                sqs.delete_message(
                    QueueUrl=job_queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            print('No messages to process. Waiting for messages...', end='\r', flush=True)
            time.sleep(5)
            # Optional: Add sleep or back-off logic here to reduce the number of empty requests


if __name__ == '__main__':
    process_messages()
