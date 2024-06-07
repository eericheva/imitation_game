from game_loop.players import GamePlayer, GamePlayerB, GamePlayerC
from setups.setup import CURRENT_USER_ID, CURRENT_USER_USERNAME
from telegram_bot_messages import telegram_bot_answers, telegram_bot_start_session
from setups.basemodel_Imitation_Game import Game


class ImitationGame(Game):
    def __init__(self):
        super().__init__()
        self.playerA = GamePlayer()
        self.playerB = GamePlayerB()
        self.playerC = GamePlayerC()

        self.game_chat_id = None
        self.last_call = None

    def start_game(self, call):
        self.playerA.setup_player(
            userid=CURRENT_USER_ID(call), username=CURRENT_USER_USERNAME(call)
        )
        self.playerB.setup_player()
        self.playerC.setup_player()
        self.game_chat_id = CURRENT_USER_ID(call)

        telegram_bot_start_session.start_game_message(call)
        self.playerC_asks_question()

    def playerC_asks_question(self):
        self.playerC.form_question()
        telegram_bot_answers.send_message(self.game_chat_id, self.playerC.last_message)
        telegram_bot_answers.ask_voiceit(
            self.game_chat_id, playername=self.playerC.username
        )
        self.playerB.form_answer(self.playerC.last_message)
        telegram_bot_answers.send_message(self.game_chat_id, self.playerB.last_message)
        telegram_bot_answers.ask_voiceit(
            self.game_chat_id, playername=self.playerB.username
        )
        telegram_bot_answers.ask_user_turn(self.game_chat_id)

    def proceed_user_message(self, call, user_message):
        self.last_call = call
        self.playerA.update_last_message(user_message)
        is_there_decision = self.playerC.try2decide(
            self.playerA.user_history, self.playerB.user_history
        )
        if not is_there_decision:
            self.playerC_asks_question()
        else:
            telegram_bot_start_session.send_decision(
                self.last_call, self.playerC.last_message
            )
