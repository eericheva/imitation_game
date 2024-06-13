import asyncio
import time

from main_setups.setup import CURRENT_USER_ID, game_d, llm_d, logger, user_d

################ USER ACTIVITY CHECK ################
from telegram_bot_messages import telegram_bot_start_session


async def user_activity_check(message):
    while user_d[CURRENT_USER_ID(message)]:
        if (time.time() - user_d[CURRENT_USER_ID(message)]) < 60:
            logger.info(
                f"inside user_activity_check {time.time() - user_d[CURRENT_USER_ID(message)]}"
            )
            await asyncio.sleep(5)
        else:
            await get_stop_command_ua(message)


async def get_stop_command_ua(message):
    game_d.pop(CURRENT_USER_ID(message), None)
    llm_d.pop(CURRENT_USER_ID(message), None)
    user_d.pop(CURRENT_USER_ID(message), None)
    await telegram_bot_start_session.message_stop_game(message)
