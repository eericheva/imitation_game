import os

import torch
from llama_cpp import Llama

from main_setups.setup import DATA_PATH, HUGGINGFACE_TOKEN


class TransformersModelLLamaCPP:
    def __init__(self, model_id, game_chat_id):
        model_gguf_path = os.path.join(DATA_PATH, model_id)
        model_path = "/".join(model_gguf_path.split("/")[:-1])
        if not os.path.exists(model_path):
            repo_id = "/".join(model_id.split("/")[:-1])
            filename = model_id.split("/")[-1]
            self.model = Llama.from_pretrained(
                repo_id=repo_id,
                filename=filename,
                local_dir=model_path,
                local_dir_use_symlinks=True,
                token=HUGGINGFACE_TOKEN,
                verbose=True,
            )
        else:
            self.model = Llama(
                model_path=model_gguf_path,
                torch_dtype=torch.bfloat16,
                n_ctx=0,
                use_mlock=True,
                flash_attn=True,
                logits_all=True,
                device_map="auto",
                token=HUGGINGFACE_TOKEN,
                verbose=True,
            )

    def query(self, input_text, base_text):
        messages = [
            {"role": "system", "content": base_text},
            {"role": "user", "content": input_text},
        ]
        outputs = self.model.create_chat_completion(
            messages=messages,
            temperature=1.0,
            top_p=0.1,
            max_tokens=256,
            repeat_penalty=1.5,
            logprobs=True,
        )
        response = outputs["choices"][0]["message"]["content"]
        response = response.strip()
        return response
