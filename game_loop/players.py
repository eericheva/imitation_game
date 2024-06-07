import json
import random

from main_setups.basemodel_Imitation_Game import Player, Prefixes
from main_setups.setup import CURRENT_USER_ID_NAME, MESSAGE_WRAPPER


# NEW USER
class GamePlayer(Player):
    def __init__(self, userid=222, username=Prefixes.PlayerA.value):
        super().__init__()
        self.userid = userid
        self.username = username

        self.last_message = None
        self.user_history = self._create_new_history()

    def _create_new_history(self):
        return []

    def _dump_user(self):
        new_user = {
            "user": {
                "id": self.userid,
                "username": self.username,
                "user_history": self.user_history,
                "last_message": self.last_message,
            }
        }
        json.dump(new_user, open(CURRENT_USER_ID_NAME(self.userid, self.username), "w"))

    def setup_player(self, userid, username):
        self.userid = userid
        self.username = username
        self._dump_user()

    def update_last_message(self, text_input):
        self.last_message = f"{MESSAGE_WRAPPER(self.username)} \n {text_input}"
        self.user_history.append(self.last_message)
        self._dump_user()


# singleton Player B
class GamePlayerB(GamePlayer):
    def __init__(self, userid=111, username=Prefixes.PlayerB.value):
        super(GamePlayerB, self).__init__(userid, username)
        self.userid = userid
        self.username = username

        self.model = None

    def setup_player(self):
        self.model = None

    def form_answer(self, text_input):
        answer = "First answer?"
        self.update_last_message(answer)


# singleton Player C
class GamePlayerC(GamePlayer):
    def __init__(self, userid=000, username=Prefixes.PlayerC.value):
        super(GamePlayerC, self).__init__(userid, username)
        self.userid = userid
        self.username = username

        self.model = None

    def setup_player(self):
        self.model = None

    def form_question(self):
        question = "First question?"
        self.update_last_message(question)

    def try2decide(self, player_a_history, player_b_history):
        text_decision = "i'm a human"
        is_there_decision = random.choice([False] * 4 + [True])
        if is_there_decision:
            self.update_last_message(text_decision)
        return is_there_decision
