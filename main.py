# coding=utf-8

from setup import basemodel_Imitation_Game
from setup.setup import CURRENT_USER_ID, game, IG_bot
from speech_tools import speech_tools
from telegram_bot_messages import telegram_bot_answers, telegram_bot_start_session


################ START SESSION ################


@IG_bot.message_handler(
    commands=[
        basemodel_Imitation_Game.BaseCommand.start.value,
        basemodel_Imitation_Game.BaseCommand.help.value,
    ]
)
def get_start_command(message):
    telegram_bot_start_session.start_me(message)


################ DIALOG MESSAGES ################


@IG_bot.message_handler(content_types=["text"])
def get_messages_text(message):
    user_text = message.text
    game.proceed_user_message(message, user_text)


@IG_bot.message_handler(content_types=["audio", "voice"])
def get_messages_voice(message):
    if message.voice.duration > 30:
        IG_bot.send_message(
            CURRENT_USER_ID(message), "NOT PROCEEDED: message is to long!"
        )
        return None
    file_info = IG_bot.get_file(message.voice.file_id)
    file_path = IG_bot.download_file(file_info.file_path)
    user_text = speech_tools.speech2text_me(file_path)
    game.proceed_user_message(message, user_text)


################ BUTTONS CHECK ################


@IG_bot.callback_query_handler(
    func=lambda call: call.data
    in [
        basemodel_Imitation_Game.GameStartItems.start_game.value,
        basemodel_Imitation_Game.GameStartItems.stop_game.value,
    ]
)
def check_button_ask_start_game(call):
    if call.data in [basemodel_Imitation_Game.GameStartItems.start_game.value]:
        game.start_game(call)
    if call.data in [basemodel_Imitation_Game.GameStartItems.stop_game.value]:
        telegram_bot_start_session.stop_game_message(call)


@IG_bot.callback_query_handler(
    func=lambda call: call.data
    in [basemodel_Imitation_Game.VoiceItItems.voiceit_item_yes.value]
)
def check_button_voiceit(call):
    telegram_bot_answers.voice_message(call, game.playerB.last_message)
    telegram_bot_answers.voice_message(call, game.playerC.last_message)


IG_bot.infinity_polling(timeout=20, long_polling_timeout=20)
