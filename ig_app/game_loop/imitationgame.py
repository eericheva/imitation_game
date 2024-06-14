from .players import GamePlayer, GamePlayerB, GamePlayerC
from main_setups import basemodel_Imitation_Game
from main_setups.setup import CURRENT_USER_ID, logger
from telegram_bot_messages import (
    telegram_bot_answers,
    telegram_bot_start_session,
)


class ImitationGame(basemodel_Imitation_Game.Game):
    def __init__(self):
        super().__init__()
        self.stop_game()

    async def start_game(self):
        await self.game_loop()

    def stop_game(self):
        self.playerA = GamePlayer()
        self.playerB = GamePlayerB()
        self.playerC = GamePlayerC()

        self.game_chat_id = None
        self.last_call = None
        self.game_status = False
        self.game_mode = None
        self.game_type = None
        self.model = None

    def setup_game_base(self, call, model):
        self.game_chat_id = CURRENT_USER_ID(call)
        self.game_status = True
        self.model = model
        self.playerA.setup_player(game_chat_id=self.game_chat_id)
        self.playerC.setup_player(game_chat_id=self.game_chat_id, model=model)
        self.playerB.setup_player(game_chat_id=self.game_chat_id, model=model)

    def setup_game_mode(self, game_mode):
        self.game_mode = game_mode

    def setup_game_type(self, game_type):
        self.game_type = game_type
        self.playerB.setup_game_type(game_type)

    def start_game_checks(self):
        if self.game_mode and self.game_type:
            return True
        else:
            return False

    def proceed_user_message_checks(self):
        if (len(self.playerC.user_history) > 0) and (
            len(self.playerB.user_history) == len(self.playerC.user_history)
        ):
            return True
        else:
            return False

    async def game_loop(self):
        # ROUND
        await telegram_bot_answers.message_send(
            self.game_chat_id,
            f"********** ROUND {len(self.playerC.user_history) + 1} ********** \n"
            f"I'm forming a question. Wait a min.",
        )
        # PlayerC
        logger.info(f"{self.game_chat_id} - playerC.form_question")
        await self.playerC.form_question(self.playerA, self.playerB)
        await telegram_bot_answers.message_send(
            self.game_chat_id, self.playerC.last_message
        )
        # PlayerA
        logger.info(f"{self.game_chat_id} - ask_user_turn")
        await telegram_bot_answers.ask_user_turn(self.game_chat_id)
        # PlayerB
        logger.info(f"{self.game_chat_id} - playerB.form_answer")
        await self.playerB.form_answer(self.playerC.last_message)
        if self.game_mode == basemodel_Imitation_Game.GameMode.full.value:
            await telegram_bot_answers.message_send(
                self.game_chat_id, self.playerB.last_message
            )
        logger.info(f"{self.game_chat_id} - playerB.form_answer finished")

    async def proceed_user_message(self, call, user_message):
        self.last_call = call
        self.playerA.update_last_message(user_message)
        await telegram_bot_answers.message_send(
            self.game_chat_id, "I'll try to decide. Wait a min"
        )
        is_there_decision, text_decision = await self.playerC.try2decide(
            self.playerA, self.playerB
        )
        if not is_there_decision:
            if self.game_mode == basemodel_Imitation_Game.GameMode.full.value:
                await telegram_bot_answers.message_intermediate_decision(
                    self.game_chat_id, text_decision
                )
            await telegram_bot_answers.message_send(
                self.game_chat_id, "Since i'm not pretty sure, i'll ask more questions"
            )
            await self.game_loop()
        else:
            self.game_status = False
            await telegram_bot_start_session.message_final_decision(
                self.last_call, self.playerC.last_message
            )
