from locust import HttpUser, task, between
from locust.env import Environment
import logging

from locust.user.wait_time import between
from locust import events
from locust.exception import StopUser

class ApiUser(HttpUser):
    wait_time = between(1, 5)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    # Define the host and api_key as class variables
    host = "http://24.52.17.82:41537/completion"
    api_key = "NSK32ECTMHHIQQ5TYA6TRI4UP"

    @task
    def stress_test(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.api_key}'}
        json = {
            "stream": False,
            "n_predict": 400,
            "temperature": 1.31,
            "stop": [
                "<|im_end|>",
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
            "prompt": "Write an article about ai"
        }
        with self.client.post(self.host, headers=headers, json=json, catch_response=True, timeout=30) as response:
            try:
                json_response_dict = response.json()
                response.raise_for_status()
                print(json_response_dict)
                response.success()
            except Exception as e:
                print('Error')
                response.failure(str(e))

@events.init.add_listener
def on_locust_init(environment: Environment, **_kwargs):
    if environment.parsed_options:
        if environment.parsed_options.host:
            ApiUser.host = environment.parsed_options.host
        if "api_key" in environment.parsed_options:
            ApiUser.api_key = environment.parsed_options.api_key

@events.test_start.add_listener
def on_test_start(environment: Environment, **_kwargs):
    if not ApiUser.api_key or not ApiUser.host:
        print("You must specify the API URL and API Key.")
        raise StopUser()
