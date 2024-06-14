import random

import openai

from main_setups.setup import LLAMA_CPP_SERVER_PORT, LLAMA_CPP_SERVER_URL


class TransformersModelOpenAI:
    def __init__(self, model_id):
        self.model = openai.AsyncOpenAI(
            api_key="sdfvkjwnefv",  # can be anything
            base_url=f"{LLAMA_CPP_SERVER_URL}:{LLAMA_CPP_SERVER_PORT}/v1"
            # base_url=f"https://llama-cpp-server-85d673e8fcdf.herokuapp.com:8080/v1"
            # NOTE: Replace with IP address and port of your llama-cpp-python server
        )

    async def query(self, input_text, base_text):
        messages = [
            {"role": "system", "content": base_text},
            {"role": "user", "content": input_text},
        ]
        outputs = await self.model.chat.completions.create(
            model="ImitationGameLlamaCPP",
            messages=messages,
            temperature=1.0,
            top_p=0.9,
            max_tokens=256,
            frequency_penalty=1.0,
            seed=random.randint(0, 100000),
        )
        response = outputs.choices[0].message.content
        response = response.strip()
        return response
