import logging
import os
import sys
import time

import telebot
from telebot.async_telebot import AsyncTeleBot

from ig_app.main_setups import basemodel_Imitation_Game

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
logger = logging.getLogger("imitation-game")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False  # to avoid doubling in logger output

############ TOKENS ############
if not os.path.exists("main_setups/telegram_bot_token.py"):
    TOKEN = os.environ.get("TOKEN")
    HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
else:
    from ig_app.main_setups.telegram_bot_token import TOKEN, HUGGINGFACE_TOKEN

############ BASEMODEL and Pathes ############
this_project_path = os.getcwd()
JSON_SCHEMA_PATH = os.path.join(
    this_project_path, "main_setups/basemodel_Imitation_Game.json"
)
json_datamodel_path = os.path.join(
    this_project_path, "main_setups/basemodel_Imitation_Game.py"
)

if not os.path.isfile(json_datamodel_path):
    os.system(
        f"datamodel-codegen  --input {JSON_SCHEMA_PATH} "
        f"--input-file-type jsonschema "
        f"--output {json_datamodel_path}  "
        f"--target-python-version 3.11.5 --use-default"
    )

DATA_PATH = os.path.join(this_project_path, "data")
if not os.path.isdir(DATA_PATH):
    os.makedirs(DATA_PATH)

############ GLOBAL VARIABLES ############

CURRENT_USER_ID = (
    lambda message: message.from_user.id
    if isinstance(message, (telebot.types.Message, telebot.types.CallbackQuery))
    else int(message.split(".")[0])
)
CURRENT_USER_USERNAME = (
    lambda message: message.from_user.username
    if isinstance(message, (telebot.types.Message, telebot.types.CallbackQuery))
    else message.split(".")[1]
)

CURRENT_USER_ID_NAME = lambda id, username: str(id) + "." + username

MESSAGE_WRAPPER = (
    lambda username: f"{username} {basemodel_Imitation_Game.MessageWrapper.says.value} : "
)

############ Elements ############
TOKEN = TOKEN
HUGGINGFACE_TOKEN = HUGGINGFACE_TOKEN

IG_bot = AsyncTeleBot(TOKEN)
# IG_bot.remove_webhook()

# other variants
# PLAYER_MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
# PLAYER_MODEL_ID = "Qwen/Qwen2-7B-Instruct"
PLAYER_MODEL_ID = (
    "second-state/Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
)

# try:
#     if not os.path.exists(os.path.join(DATA_PATH, PLAYER_MODEL_ID)):
#         logger.info(f"loading {PLAYER_MODEL_ID}")
#         snapshot_download(
#             repo_id=PLAYER_MODEL_ID,
#             local_dir=os.path.join(DATA_PATH, PLAYER_MODEL_ID),
#             local_dir_use_symlinks=True,
#             token=HUGGINGFACE_TOKEN,
#             # force_download = True
#         )
# except:
#     if not os.path.exists(os.path.join(DATA_PATH, PLAYER_MODEL_ID)):
#         logger.info(f"loading {PLAYER_MODEL_ID}")
#         snapshot_download(
#             repo_id=PLAYER_MODEL_ID,
#             local_dir=os.path.join(DATA_PATH, PLAYER_MODEL_ID),
#             local_dir_use_symlinks=True,
#             token=HUGGINGFACE_TOKEN,
#             force_download=True,
#         )

game_d = {}
llm_d = {}
nonactive_user_d = {}


def set_new_nonactive_user_d(message):
    nonactive_user_d[CURRENT_USER_ID(message)] = time.time()


MAX_NUM_USERS = 1
TIME_NONACTIV_USER_KICK = 5 * 60

logger.info(f"SETUP FINISHED")
