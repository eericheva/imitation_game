import os

import telebot

from main_setups import basemodel_Imitation_Game

############ TOKENS ############
if not os.path.exists("main_setups/telegram_bot_token.py"):
    TOKEN = os.environ.get("TOKEN")
else:
    from main_setups.telegram_bot_token import TOKEN

############ Elements ############
IG_bot = telebot.TeleBot(TOKEN)
IG_bot.remove_webhook()

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
        f"--target-python-version 3.8 --use-default"
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

# dailySerbian_updater = Updater(TOKEN, use_context=True)
# dailySerbian_dispatcher = dailySerbian_updater.dispatcher
