import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ig_app.main_setups.setup import DATA_PATH, HUGGINGFACE_TOKEN
from ig_app.telegram_bot_messages import telegram_bot_answers


class TransformersModel:
    def __init__(self, model_id, game_chat_id):
        telegram_bot_answers.message_send(
            game_chat_id, f"Please, wait! I am waking up right now."
        )
        model_path = os.path.join(DATA_PATH, model_id)
        model_path = model_path if os.path.exists(model_path) else model_id
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, token=HUGGINGFACE_TOKEN
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            token=HUGGINGFACE_TOKEN,
        )
        telegram_bot_answers.message_send(game_chat_id, "i'm here, let's continue!")

    def query(self, input_text, base_text):
        messages = [
            {"role": "system", "content": base_text},
            {"role": "user", "content": input_text},
        ]
        input_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        )
        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=256,
            eos_token_id=terminators,
            pad_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        generated_ids = outputs[0][input_ids.shape[-1] :]
        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response
