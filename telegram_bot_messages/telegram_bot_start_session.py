import telebot

from main_setups import basemodel_Imitation_Game
from main_setups.setup import CURRENT_USER_ID, IG_bot
from telegram_bot_messages.telegram_bot_answers import ask_voiceit


def start_me(message):
    IG_bot.send_message(CURRENT_USER_ID(message), "Hello! What is going on here:")

    IG_bot.send_message(
        CURRENT_USER_ID(message),
        f"Here are three players. Player A is you, Player B is the invited AI bot, and Player C is me, "
        f"the AI bot acting as the conversation host. \n"
        f"According to the rules of the game, I don't know which of Players A and B is the bot and which is the "
        f"human, and I can only communicate with you through written messages. \n"
        f"By asking questions to Players A and B, I will try to determine who is the bot and who is the human. \n"
        f"Your task is to confuse me, pretending to be the bot so that I make the wrong conclusion. \n"
        f"At the same time, the invited AI bot's task is to help me make the correct judgment and "
        f"correctly identify which player is the human. \n",
    )
    ask_start_game(message)


def ask_start_game(call):
    item_yes = telebot.types.InlineKeyboardButton(
        text="Start!",
        callback_data=basemodel_Imitation_Game.GameStartItems.start_game.value,
    )
    item_no = telebot.types.InlineKeyboardButton(
        text="May be latter...",
        callback_data=basemodel_Imitation_Game.GameStartItems.stop_game.value,
    )
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
    IG_bot.send_message(
        CURRENT_USER_ID(call),
        "Wanna play?",
        reply_markup=markup,
    )


def start_game_message(message):
    IG_bot.send_message(
        CURRENT_USER_ID(message),
        f"Hooray, let's beggin ",
    )


def ask_game_mode(call):
    item_yes = telebot.types.InlineKeyboardButton(
        text="Blind",
        callback_data=basemodel_Imitation_Game.GameMode.blind.value,
    )
    item_no = telebot.types.InlineKeyboardButton(
        text="Explanatory",
        callback_data=basemodel_Imitation_Game.GameMode.full.value,
    )
    markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
    IG_bot.send_message(
        CURRENT_USER_ID(call),
        """
                In which mode will we play?

        **Blind** means - Player A (you) cannot see Player B's answers or Player C's reasoning about how they make
        decisions
        after each answer.

        **Explanatory** means - before Player A is given the opportunity to answer, they will see Player B's
        response. After
        each series of questions and answers, Player C's reasoning for making their decision will be shown.
                """,
        reply_markup=markup,
    )


def stop_game_message(message):
    IG_bot.send_message(
        CURRENT_USER_ID(message),
        f"Maybe next time. Bye",
    )


def send_decision(message, text_input):
    IG_bot.send_message(
        chat_id=CURRENT_USER_ID(message),
        text="********************* \n I an ready make a decision \n *********************",
    )
    IG_bot.send_message(chat_id=CURRENT_USER_ID(message), text=text_input)
    ask_voiceit(
        CURRENT_USER_ID(message), basemodel_Imitation_Game.Prefixes.PlayerC.value
    )
    ask_start_game(message)
