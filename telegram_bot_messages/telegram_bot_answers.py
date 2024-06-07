import telebot

from setups import basemodel_Imitation_Game
from setups.setup import IG_bot, MESSAGE_WRAPPER
from speech_tools.speech_tools import text2speech_me


def send_message(chat_id, text_input):
    IG_bot.send_message(chat_id=chat_id, text=text_input)


def voice_message(chat_id, text_input):
    voice = text2speech_me(chat_id=chat_id, input=text_input)
    IG_bot.send_voice(chat_id=chat_id, voice=voice)
    ask_user_turn(chat_id)


def ask_voiceit(chat_id, playername):
    if playername == basemodel_Imitation_Game.Prefixes.PlayerC.value:
        item_yes = telebot.types.InlineKeyboardButton(
            text="Yes!",
            callback_data=basemodel_Imitation_Game.VoiceItItems.voice_c_yes.value,
        )
    if playername == basemodel_Imitation_Game.Prefixes.PlayerB.value:
        item_yes = telebot.types.InlineKeyboardButton(
            text="Yes!",
            callback_data=basemodel_Imitation_Game.VoiceItItems.voice_b_yes.value,
        )
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes)
    IG_bot.send_message(
        chat_id=chat_id,
        text="Wanna listen?",
        reply_markup=markup,
    )


def ask_user_turn(chat_id):
    text_input = "You turn. \n" + MESSAGE_WRAPPER(
        basemodel_Imitation_Game.Prefixes.PlayerA.value
    )
    IG_bot.send_message(chat_id=chat_id, text=text_input)
