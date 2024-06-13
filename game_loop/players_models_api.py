import requests
from huggingface_hub import InferenceApi, InferenceClient

from main_setups.setup import HUGGINGFACE_TOKEN
from telegram_bot_messages import telegram_bot_answers


class InferenceAPIModel:
    def __init__(self, model_id, game_chat_id):
        self.model_id = model_id
        self.game_chat_id = game_chat_id
        self.model = InferenceApi(
            repo_id=self.model_id, task="text-generation", token=HUGGINGFACE_TOKEN
        )

    def query(self, input_text):
        response = self.model(
            input_text, params={"return_full_text": False, "wait_for_model": True}
        )
        return response


class InferenceAPIRequestModel:
    def __init__(self, model_id, game_chat_id):
        self.model_id = model_id
        self.game_chat_id = game_chat_id
        self.query("hello", first_wake_up=True)

    def query(self, input_text, first_wake_up=False):
        # simple for
        # PLAYER_B_MODEL_ID = "OpenBuddy/openbuddy-zen-3b-v21.2-32k"
        # PLAYER_C_MODEL_ID = "OpenBuddy/openbuddy-zen-3b-v21.2-32k"
        payload = {
            "inputs": input_text,
            "parameters": {"return_full_text": False, "wait_for_model": True}
            # "option":     {"wait_for_model": "true"}
        }

        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        API_URL = f"https://api-inference.huggingface.co/models/{self.model_id}"
        response = requests.post(API_URL, headers=headers, json=payload)
        while response.status_code == 503:
            telegram_bot_answers.message_send(
                self.game_chat_id,
                f"Please, wait! I am waking up right now. Estimated Time: "
                f"{response.json().get('estimated_time')}",
            )
            # time.sleep(response.json().get('estimated_time'))
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                telegram_bot_answers.message_send(
                    self.game_chat_id, "i'm here, let's continue!"
                )
                response = (
                    response.json()[0].get("generated_text")
                    if not first_wake_up
                    else ""
                )
                break
        return response


class InferenceClientModel:
    def __init__(self, model_id, game_chat_id):
        self.model_id = model_id
        self.game_chat_id = game_chat_id
        self.model = InferenceClient(model=self.model_id, token=HUGGINGFACE_TOKEN)

    def query(self, input_text):
        response = self.model.text_generation(
            input_text, max_new_tokens=40, return_full_text=False
        )
        return response
