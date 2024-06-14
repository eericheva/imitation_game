import telebot

from main_setups import basemodel_Imitation_Game
from main_setups.setup import CURRENT_USER_ID, IG_bot
from telegram_bot_messages.telegram_bot_user_activity_check import (
    user_activity_check,
)


async def ask_start_new_session(message):
    await _greet_me(message)
    await _ask_start_game(message)
    await user_activity_check(message)


async def message_wait_new_session(message):
    await _greet_me(message)
    input_text = (
        "Too many users right now. I can't handle one more((( Pls, try later again"
    )
    await IG_bot.send_message(CURRENT_USER_ID(message), input_text)
    await message_stop_game(message)


async def _greet_me(message):
    await IG_bot.send_message(CURRENT_USER_ID(message), "Hello! What is going on here:")
    input_text = (
        f"Here are three players. Player A is you, Player B is the invited AI bot, and Player C is me, "
        f"the AI bot acting as the conversation host. \n"
        f"According to the rules of the game, I don't know which of Players A and B is the bot and which is "
        f"the human, and I can only communicate with you through written messages. \n"
        f"By asking questions to Players A and B, I will try to determine who is the bot and who is the "
        f"human. \n"
        f"Your task is to confuse me, pretending to be the bot (or a human) so that I make the "
        f"wrong conclusion. \n"
        f"At the same time, the Player B's (bot) task is to help me make the correct judgment and "
        f"correctly identify which player is the human. \n"
    )
    await IG_bot.send_message(CURRENT_USER_ID(message), input_text)


async def _ask_start_game(call):
    item_yes = telebot.types.InlineKeyboardButton(
        text="Start!",
        callback_data=basemodel_Imitation_Game.GameStartItems.start_game.value,
    )
    item_no = telebot.types.InlineKeyboardButton(
        text="May be latter...",
        callback_data=basemodel_Imitation_Game.GameStartItems.stop_game.value,
    )
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
    input_text = "Wanna play again?"
    await IG_bot.send_message(CURRENT_USER_ID(call), input_text, reply_markup=markup)


async def ask_game_type(call):
    item_yes = telebot.types.InlineKeyboardButton(
        text="Direct",
        callback_data=basemodel_Imitation_Game.GameType.direct.value,
    )
    item_no = telebot.types.InlineKeyboardButton(
        text="Inverse",
        callback_data=basemodel_Imitation_Game.GameType.inverse.value,
    )
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
    input_text = (
        "There are two types of imitation games possible. \n "
        "**Direct** imitation game - Player A and Player B both pretend to be humans. \n"
        "**Inverse** imitation game - both players pretend to be bots. \n "
        "Which one you wanna play?"
    )
    await IG_bot.send_message(CURRENT_USER_ID(call), input_text, reply_markup=markup)


async def ask_game_mode(call):
    item_yes = telebot.types.InlineKeyboardButton(
        text="Blind", callback_data=basemodel_Imitation_Game.GameMode.blind.value
    )
    item_no = telebot.types.InlineKeyboardButton(
        text="Explanatory", callback_data=basemodel_Imitation_Game.GameMode.full.value
    )
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
    input_text = (
        "In which mode will we play? \n"
        "**Blind** means - Player A (you) cannot see Player B's answers or Player C's reasoning about "
        "how they make decisions after each answer. \n"
        "**Explanatory** means - before Player A is given the opportunity to answer, they will "
        "see Player B's response. After each series of questions and answers, Player C's reasoning "
        "for making their decision will be shown."
    )
    await IG_bot.send_message(CURRENT_USER_ID(call), input_text, reply_markup=markup)


async def message_start_game(message):
    await IG_bot.send_message(
        CURRENT_USER_ID(message),
        f"Hooray!! All setup is done! Let's beggin... ",
    )


async def message_stop_game(message):
    await IG_bot.send_message(
        CURRENT_USER_ID(message),
        "We'll play next time. Bye \n "
        f"To start new game send me /{basemodel_Imitation_Game.BaseCommand.start.value}",
    )


async def message_final_decision(message, text_input):
    await IG_bot.send_message(
        chat_id=CURRENT_USER_ID(message),
        text="********************* \n I am ready make a decision \n *********************",
    )
    await IG_bot.send_message(chat_id=CURRENT_USER_ID(message), text=text_input)
    await _ask_start_game(message)
