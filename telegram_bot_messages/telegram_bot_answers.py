import telebot

from setup import basemodel_Imitation_Game
from setup.setup import IG_bot, MESSAGE_WRAPPER
from speech_tools.speech_tools import text2speech_me


def send_message(chat_id, text_input):
    IG_bot.send_message(chat_id=chat_id, text=text_input)
    ask_voiceit(chat_id)


def voice_message(chat_id, text_input):
    voice = text2speech_me(chat_id=chat_id, input=text_input)
    IG_bot.send_voice(chat_id=chat_id, voice=voice)


def ask_voiceit(chat_id):
    item_yes = telebot.types.InlineKeyboardButton(
        text="Yes!",
        callback_data=basemodel_Imitation_Game.VoiceItItems.voiceit_item_yes.value,
    )
    # item_no = telebot.types.InlineKeyboardButton(
    #         text="May be latter...",
    #         callback_data=basemodel_Imitation_Game.GameStartItems.stop_game.value,
    #         )
    # markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes)
    IG_bot.send_message(
        chat_id=chat_id,
        text="Wanna listen?",
        reply_markup=markup,
    )


def ask_user_turn(chat_id):
    IG_bot.send_message(chat_id=chat_id, text="You turn.")
    text_input = MESSAGE_WRAPPER(basemodel_Imitation_Game.Prefixes.PlayerA.value)
    IG_bot.send_message(chat_id=chat_id, text=text_input)
