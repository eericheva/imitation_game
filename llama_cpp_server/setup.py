import logging
import os
import sys

from huggingface_hub import hf_hub_download

########### LOGER ###########
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="**************** \n "
    "%(asctime)s - %(levelname)s - %(message)s \n"
    "****************",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger = logging.getLogger("llama-cpp-server")
logger.handlers.clear()  # to avoid doubling in logger output
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False  # to avoid doubling in logger output

############ TOKENS ############
if not os.path.exists("main_setups/telegram_bot_token.py"):
    HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
else:
    from telegram_bot_token import HUGGINGFACE_TOKEN

############ BASEMODEL and Pathes ############
this_project_path = os.getcwd()
DATA_PATH = os.path.join(this_project_path, "data")
if not os.path.isdir(DATA_PATH):
    os.makedirs(DATA_PATH)

############ Elements ############
HUGGINGFACE_TOKEN = HUGGINGFACE_TOKEN

# other variants
# PLAYER_MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
# PLAYER_MODEL_ID = "Qwen/Qwen2-7B-Instruct"
REPO_ID = "second-state/Llama-3-8B-Instruct-GGUF"
FILENAME = "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
PLAYER_MODEL_ID = os.path.join(REPO_ID, FILENAME)

try:
    if not os.path.exists(os.path.join(DATA_PATH, PLAYER_MODEL_ID)):
        logger.info(f"loading {PLAYER_MODEL_ID}")
        hf_hub_download(
            repo_id=REPO_ID,
            filename=FILENAME,
            local_dir=os.path.join(DATA_PATH, REPO_ID),
            token=HUGGINGFACE_TOKEN
            # force_download = True
        )
except:
    if not os.path.exists(os.path.join(DATA_PATH, PLAYER_MODEL_ID)):
        logger.info(f"loading {PLAYER_MODEL_ID}")
        hf_hub_download(
            repo_id=REPO_ID,
            filename=FILENAME,
            local_dir=os.path.join(DATA_PATH, REPO_ID),
            token=HUGGINGFACE_TOKEN,
            force_download=True,
        )

logger.info(f"SETUP FINISHED")
