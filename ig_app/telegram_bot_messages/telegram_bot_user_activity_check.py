import asyncio
import time

from main_setups.setup import (
    CURRENT_USER_ID,
    game_d,
    llm_d,
    logger,
    nonactive_user_d,
    TIME_NONACTIV_USER_KICK,
)

################ USER ACTIVITY CHECK ################
from telegram_bot_messages import telegram_bot_start_session


async def user_activity_check(message):
    while nonactive_user_d[CURRENT_USER_ID(message)]:
        if (
            time.time() - nonactive_user_d[CURRENT_USER_ID(message)]
        ) < TIME_NONACTIV_USER_KICK:
            logger.info(
                f"{CURRENT_USER_ID(message)} - inside user_activity_check - "
                f"{time.time() - nonactive_user_d[CURRENT_USER_ID(message)]}"
            )
            await asyncio.sleep(30)
        else:
            await get_stop_command_ua(message)


async def get_stop_command_ua(message):
    game_d.pop(CURRENT_USER_ID(message), None)
    llm_d.pop(CURRENT_USER_ID(message), None)
    nonactive_user_d.pop(CURRENT_USER_ID(message), None)
    logger.info(f"{CURRENT_USER_ID(message)} - get_stop_command_ua")
    await telegram_bot_start_session.message_stop_game(message)
