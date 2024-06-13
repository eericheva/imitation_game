import random

import openai


class TransformersModelOpenAI:
    def __init__(self, model_id):
        self.model = openai.AsyncOpenAI(
            api_key="sdfvkjwnefv",  # can be anything
            base_url="http://0.0.0.0:8080/v1"
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
