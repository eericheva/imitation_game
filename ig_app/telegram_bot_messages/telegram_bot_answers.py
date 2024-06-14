import telebot

from ig_app.main_setups import basemodel_Imitation_Game
from ig_app.main_setups.setup import IG_bot, MESSAGE_WRAPPER
from ig_app.speech_tools.speech_tools import text2speech_me


async def message_send(chat_id, text_input):
    await IG_bot.send_message(chat_id=chat_id, text=text_input)
    # ask_voiceit(chat_id, playername)


async def message_voice(chat_id, text_input):
    voice = text2speech_me(chat_id=chat_id, input=text_input)
    await IG_bot.send_voice(chat_id=chat_id, voice=voice)


async def ask_voiceit(chat_id, playername):
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
    await IG_bot.send_message(
        chat_id=chat_id,
        text="Wanna listen?",
        reply_markup=markup,
    )


async def ask_user_turn(chat_id):
    text_input = "You can answer now. \n" + MESSAGE_WRAPPER(
        basemodel_Imitation_Game.Prefixes.PlayerA.value
    )
    await IG_bot.send_message(chat_id=chat_id, text=text_input)


async def message_wait_playerb_answer(chat_id):
    text_input = f"Player B is answering. Wait for a min"
    await IG_bot.send_message(chat_id=chat_id, text=text_input)


async def message_intermediate_decision(chat_id, text_input):
    await IG_bot.send_message(
        chat_id=chat_id,
        text="********************* \n Here is my intermediate decision \n *********************",
    )
    await IG_bot.send_message(chat_id=chat_id, text=text_input)
