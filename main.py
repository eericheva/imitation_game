# coding=utf-8
import asyncio
import time

from game_loop.imitationgame import ImitationGame
from game_loop.players_models_llamacpp import TransformersModelLLamaCPP
from main_setups import basemodel_Imitation_Game
from main_setups.setup import (
    CURRENT_USER_ID,
    game_d,
    IG_bot,
    llm_d,
    MAX_NUM_USERS,
    PLAYER_C_MODEL_ID,
    set_new_user_d,
    user_d,
)
from speech_tools import speech_tools
from telegram_bot_messages import (
    telegram_bot_answers,
    telegram_bot_start_session,
    telegram_bot_user_activity_check,
)


################ START SESSION ################


@IG_bot.message_handler(
    commands=[
        basemodel_Imitation_Game.BaseCommand.start.value,
        basemodel_Imitation_Game.BaseCommand.help.value,
    ]
)
async def get_start_command(message):
    if CURRENT_USER_ID(message) not in game_d:
        if len(game_d) > MAX_NUM_USERS:
            await telegram_bot_start_session.message_wait_new_session(message)
        else:
            new_user(message)
            await telegram_bot_start_session.ask_start_new_session(message)
    else:
        await telegram_bot_start_session.ask_start_new_session(message)


@IG_bot.message_handler(
    commands=[
        basemodel_Imitation_Game.GameStartItems.stop_game.value,
    ]
)
async def get_stop_command(message):
    await telegram_bot_user_activity_check.get_stop_command_ua(message)


################ DIALOG MESSAGES ################
@IG_bot.message_handler(content_types=["text"])
async def get_messages_text(message):
    if CURRENT_USER_ID(message) not in game_d:
        if len(game_d) > MAX_NUM_USERS:
            await telegram_bot_start_session.message_wait_new_session(message)
        else:
            new_user(message)
            await telegram_bot_start_session.ask_start_new_session(message)
    else:
        set_new_user_d(message)
        if game_d[CURRENT_USER_ID(message)].game_status:
            user_text = message.text
            if not game_d[CURRENT_USER_ID(message)].proceed_user_message_checks():
                await telegram_bot_answers.message_wait_playerb_answer(
                    game_d[CURRENT_USER_ID(message)].game_chat_id
                )
            while not game_d[CURRENT_USER_ID(message)].proceed_user_message_checks():
                await asyncio.sleep(5)
            set_new_user_d(message)
            await game_d[CURRENT_USER_ID(message)].proceed_user_message(
                message, user_text
            )
        else:
            await get_start_command(message)


@IG_bot.message_handler(content_types=["audio", "voice"])
async def get_messages_voice(message):
    if CURRENT_USER_ID(message) not in game_d:
        if len(game_d) > MAX_NUM_USERS:
            await telegram_bot_start_session.message_wait_new_session(message)
        else:
            new_user(message)
            await telegram_bot_start_session.ask_start_new_session(message)
    else:
        set_new_user_d(message)
        if game_d[CURRENT_USER_ID(message)].game_status:
            if message.voice.duration > 30:
                await telegram_bot_answers.message_send(
                    CURRENT_USER_ID(message), "NOT PROCEEDED: message is to long!"
                )
                return None
            file_info = IG_bot.get_file(message.voice.file_id)
            file_path = IG_bot.download_file(file_info.file_path)
            user_text = speech_tools.speech2text_me(file_path)
            if not game_d[CURRENT_USER_ID(message)].proceed_user_message_checks():
                await telegram_bot_answers.message_wait_playerb_answer(
                    game_d[CURRENT_USER_ID(message)].game_chat_id
                )
            while not game_d[CURRENT_USER_ID(message)].proceed_user_message_checks():
                await asyncio.sleep(5)
            set_new_user_d(message)
            await game_d[CURRENT_USER_ID(message)].proceed_user_message(
                message, user_text
            )
        else:
            await get_start_command(message)


################ BUTTONS CHECK ################
################ BUTTONS start game ################


@IG_bot.callback_query_handler(
    func=lambda call: call.data
    in [
        basemodel_Imitation_Game.GameStartItems.start_game.value,
        basemodel_Imitation_Game.GameStartItems.stop_game.value,
    ]
)
async def check_button_ask_start_game(call):
    if call.data in [basemodel_Imitation_Game.GameStartItems.start_game.value]:
        if CURRENT_USER_ID(call) not in game_d:
            if len(game_d) > MAX_NUM_USERS:
                await telegram_bot_start_session.message_wait_new_session(call)
            else:
                new_user(call)
        else:
            game_d[CURRENT_USER_ID(call)].stop_game()
            user_d[CURRENT_USER_ID(call)] = time.time()
            await telegram_bot_start_session.ask_game_mode(call)
            await telegram_bot_start_session.ask_game_type(call)
            game_d[CURRENT_USER_ID(call)].setup_game_base(
                call, llm_d[CURRENT_USER_ID(call)]
            )
            while not game_d[CURRENT_USER_ID(call)].start_game_checks():
                await asyncio.sleep(5)
            await telegram_bot_start_session.message_start_game(call)
            await game_d[CURRENT_USER_ID(call)].start_game()
    if call.data in [basemodel_Imitation_Game.GameStartItems.stop_game.value]:
        await get_stop_command(call)


################ BUTTONS setup game ################


@IG_bot.callback_query_handler(
    func=lambda call: call.data
    in [
        basemodel_Imitation_Game.GameMode.blind.value,
        basemodel_Imitation_Game.GameMode.full.value,
    ]
)
async def check_button_ask_game_mode(call):
    await telegram_bot_answers.message_send(
        CURRENT_USER_ID(call),
        f"We'll play **{call.data}** mode.",
    )
    game_d[CURRENT_USER_ID(call)].setup_game_mode(call.data)
    user_d[CURRENT_USER_ID(call)] = time.time()


@IG_bot.callback_query_handler(
    func=lambda call: call.data
    in [
        basemodel_Imitation_Game.GameType.direct.value,
        basemodel_Imitation_Game.GameType.inverse.value,
    ]
)
async def check_button_ask_game_type(call):
    await telegram_bot_answers.message_send(
        CURRENT_USER_ID(call),
        f"We'll play **{call.data}** imitation game.",
    )
    game_d[CURRENT_USER_ID(call)].setup_game_type(call.data)
    user_d[CURRENT_USER_ID(call)] = time.time()


def new_user(message):
    llm_d[CURRENT_USER_ID(message)] = TransformersModelLLamaCPP(
        model_id=PLAYER_C_MODEL_ID
    )
    game_d[CURRENT_USER_ID(message)] = ImitationGame()
    set_new_user_d(message)


asyncio.run(IG_bot.infinity_polling())

################ BUTTONS voice it ################

# @IG_bot.callback_query_handler(
#         func=lambda call: call.data
#                           in [
#                                   basemodel_Imitation_Game.VoiceItItems.voice_c_yes.value,
#                                   basemodel_Imitation_Game.VoiceItItems.voice_b_yes.value,
#                                   ]
#         )
# def check_button_voiceit(call):
#     if call.data in [basemodel_Imitation_Game.VoiceItItems.voice_c_yes.value]:
#         telegram_bot_answers.message_send(
#                 CURRENT_USER_ID(call), MESSAGE_WRAPPER(game.playerC.username)
#                 )
#         telegram_bot_answers.message_voice(
#                 CURRENT_USER_ID(call), game.playerC.last_message
#                 )
#     if call.data in [basemodel_Imitation_Game.VoiceItItems.voice_b_yes.value]:
#         telegram_bot_answers.message_send(
#                 CURRENT_USER_ID(call), MESSAGE_WRAPPER(game.playerB.username)
#                 )
#         telegram_bot_answers.message_voice(
#                 CURRENT_USER_ID(call), game.playerB.last_message
#                 )
