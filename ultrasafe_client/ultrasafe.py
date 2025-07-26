import os
import requests
from dotenv import load_dotenv

load_dotenv()


class UltraSafe:
    class Chat:
        class Completions:
            def __init__(self):

                self.api_key = os.getenv("ULTRASAFE_API_KEY")
                if not self.api_key:
                    raise ValueError("ULTRASAFE_API_KEY environment variable not set.")
            @staticmethod
            def create(model, messages, temperature=0.7, max_tokens=1000, web_search=True, stream=False):
                """
                Mimics the OpenAI API's chat.completions.create method.
                Sends a request to the UltraSafe API and returns the response.
                """
                api_url = "https://api.us.inc/usf/v1/hiring/chat/completions"  
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.getenv('ULTRASAFE_API_KEY')}",  
                }
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "web_search": web_search,
                    "stream": stream,
                    "max_tokens": max_tokens
                }

                try:
                    response = requests.post(api_url, headers=headers, json=payload)
                    response.raise_for_status() 
                    response_data = response.json()
                    
                    return response_data
                except requests.exceptions.RequestException as e:
                    print(f"API Request Error: {e}")
                    return None
                except KeyError as e:
                    print(f"Unexpected API Response Format: {e}")
                    return None

    chat = Chat()