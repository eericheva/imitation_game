import os
import random

import torch
from llama_cpp import Llama

from ig_app.main_setups.setup import DATA_PATH, HUGGINGFACE_TOKEN


class TransformersModelLLamaCPP:
    def __init__(self, model_id):
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
                verbose=False,
            )
        else:
            self.model = Llama(
                model_path=model_gguf_path,
                torch_dtype=torch.bfloat16,
                n_ctx=0,
                n_threads=16,
                use_mlock=True,
                flash_attn=True,
                # logits_all=True,
                # device_map="auto",
                token=HUGGINGFACE_TOKEN,
                verbose=False,
            )

    async def query(self, input_text, base_text):
        messages = [
            {"role": "system", "content": base_text},
            {"role": "user", "content": input_text},
        ]
        outputs = self.model.create_chat_completion(
            messages=messages,
            temperature=1.0,
            top_p=0.9,
            max_tokens=256,
            repeat_penalty=1.5,
            # logprobs=True,
            seed=random.randint(0, 100000),
        )
        response = outputs["choices"][0]["message"]["content"]
        response = response.strip()
        return response
