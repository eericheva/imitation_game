import os

import intel_extension_for_pytorch as ipex
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ig_app.main_setups.setup import DATA_PATH, HUGGINGFACE_TOKEN, logger
from ig_app.telegram_bot_messages import telegram_bot_answers


class TransformersModelWOQ:
    def __init__(self, model_id, game_chat_id):
        telegram_bot_answers.message_send(
            game_chat_id, f"Please, wait! I am waking up right now."
        )
        model_woq_path = os.path.join(DATA_PATH, model_id + "-WOQ.pt")
        model_path = os.path.join(DATA_PATH, model_id)
        model_path = model_path if os.path.exists(model_path) else model_id

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, token=HUGGINGFACE_TOKEN
        )
        if not os.path.exists(model_woq_path):
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                token=HUGGINGFACE_TOKEN,
            )
            qconfig = ipex.quantization.get_weight_only_quant_qconfig_mapping(
                weight_dtype=torch.quint4x2,  # or torch.qint8
                lowp_mode=ipex.quantization.WoqLowpMode.NONE,  # or FP16, BF16, INT8
            )
            checkpoint = None  # optionally load int4 or int8 checkpoint

            # Model optimization and quantization
            logger.info(
                f"{model_id} optimization and quantization. Time expected: 2 min"
            )
            self.model = ipex.llm.optimize(
                self.model,
                quantization_config=qconfig,
                low_precision_checkpoint=checkpoint,
            )
            # Save the quantized model
            # logger.info(f"{model_id} save the quantized model")
            # torch.jit.save(torch.jit.script(self.model), model_woq_path)
            # self.model.save_pretrained(model_woq_path, from_pt=False)
            # from_tf=False to indicate that the model is not a TensorFlow checkpoint
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_woq_path, from_tf=False
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

        with torch.inference_mode():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=256,
                eos_token_id=terminators[0],
                pad_token_id=terminators[0],
                repetition_penalty=1.5,
                # do_sample=True,
                # temperature=0.6,
                # top_p=0.9,
            )
            #   File "/home/user/eericheva/venv_ig/lib/python3.11/site-packages/transformers/generation/utils.py",
            #   line 2811, in sample
            #     next_token_logits = outputs.logits[:, -1, :]
            #                         ^^^^^^^^^^^^^^
            # AttributeError: 'tuple' object has no attribute 'logits'
        generated_ids = outputs[0][input_ids.shape[-1] :]
        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response
