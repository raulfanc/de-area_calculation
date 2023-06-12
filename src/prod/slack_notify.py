import os
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
client = WebClient(token=SLACK_TOKEN)


def send_notification(message: str):
    try:
        response = client.chat_postMessage(
            channel='#testing-notification-with-python',
            text=message,
        )
        assert response["message"]["text"] == message

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

