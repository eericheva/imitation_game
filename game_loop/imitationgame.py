from game_loop.players import GamePlayer, GamePlayerB, GamePlayerC
from main_setups import basemodel_Imitation_Game
from main_setups.basemodel_Imitation_Game import Game
from main_setups.setup import CURRENT_USER_ID
from telegram_bot_messages import telegram_bot_answers, telegram_bot_start_session


class ImitationGame(Game):
    def __init__(self):
        super().__init__()
        self.playerA = GamePlayer()
        self.playerB = GamePlayerB()
        self.playerC = GamePlayerC()

        self.game_chat_id = None
        self.last_call = None
        self.game_status = False
        self.game_mode = None

    def start_game(self, call):
        self.game_chat_id = CURRENT_USER_ID(call)
        self.game_status = True
        self.playerA.setup_player(game_chat_id=self.game_chat_id)
        self.playerC.setup_player(game_chat_id=self.game_chat_id)
        self.playerB.setup_player(game_chat_id=self.game_chat_id)

        telegram_bot_start_session.start_game_message(call)
        telegram_bot_start_session.ask_game_mode(call)
        self.game_loop()

    def game_loop(self):
        self.playerC.form_question(self.playerA, self.playerB)
        telegram_bot_answers.send_message(self.game_chat_id, self.playerC.last_message)
        telegram_bot_answers.ask_voiceit(
            self.game_chat_id, playername=self.playerC.username
        )
        telegram_bot_answers.send_message(
            self.game_chat_id,
            f"{self.playerB.username} is answering. Wait a min for 'You turn' command",
        )
        self.playerB.form_answer(self.playerC.last_message)
        if self.game_mode == basemodel_Imitation_Game.GameMode.full.value:
            telegram_bot_answers.send_message(
                self.game_chat_id, self.playerB.last_message
            )
            telegram_bot_answers.ask_voiceit(
                self.game_chat_id, playername=self.playerB.username
            )
        telegram_bot_answers.ask_user_turn(self.game_chat_id)

    def proceed_user_message(self, call, user_message):
        self.last_call = call
        self.playerA.update_last_message(user_message)
        telegram_bot_answers.send_message(
            self.game_chat_id, "I'll try to decide. Wait a min"
        )
        is_there_decision, text_decision = self.playerC.try2decide(
            self.playerA, self.playerB
        )
        if not is_there_decision:
            if self.game_mode == basemodel_Imitation_Game.GameMode.full.value:
                telegram_bot_answers.send_message(self.game_chat_id, text_decision)
            telegram_bot_answers.send_message(
                self.game_chat_id, "Since i'm not pretty sure, i'll ask more questions"
            )
            self.game_loop()
        else:
            self.game_status = False
            telegram_bot_start_session.send_decision(
                self.last_call, self.playerC.last_message
            )
