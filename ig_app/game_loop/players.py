import re

from ig_app.game_loop.players_prompts_hf import (
    prompt_answer_player_b,
    prompt_base_full_desicion_player_c,
    prompt_base_player_b,
    prompt_base_question_player_c,
    prompt_base_try_get_confidence_player_c,
    prompt_base_try_get_decision_player_c,
    prompt_full_desicion_player_c,
    prompt_question_player_c,
    prompt_try_get_confidence_player_c,
    prompt_try_get_decision_player_c,
)
from ig_app.main_setups import basemodel_Imitation_Game
from ig_app.main_setups.setup import (
    logger,
    MESSAGE_WRAPPER,
)


# NEW USER
class GamePlayer(basemodel_Imitation_Game.Player):
    def __init__(self, username=basemodel_Imitation_Game.Prefixes.PlayerA.value):
        super().__init__()
        self.username = username

        self.last_message = None
        self.user_history = self._create_new_history()

        self.model = None
        self.game_chat_id = None

    def _create_new_history(self):
        return []

    def setup_player(self, game_chat_id, model=None):
        self.model = None
        self.game_chat_id = game_chat_id

    def update_last_message(self, text_input):
        self.last_message = f"{MESSAGE_WRAPPER(self.username)} \n {text_input}"
        self.user_history.append(self.last_message)


# singleton Player B
class GamePlayerB(GamePlayer):
    def __init__(self, username=basemodel_Imitation_Game.Prefixes.PlayerB.value):
        super(GamePlayerB, self).__init__(username)
        self.username = username
        self.model = None
        self.game_type = None
        self.game_chat_id = None

    def setup_player(self, game_chat_id, model=None):
        self.model = model
        self.game_chat_id = game_chat_id

    def setup_game_type(self, game_type):
        self.game_type = game_type

    async def form_answer(self, text_input):
        prompt_base = prompt_base_player_b()
        if self.game_type == basemodel_Imitation_Game.GameType.direct.value:
            prompt_base = prompt_base_player_b()
        prompt = prompt_answer_player_b(text_input)
        answer = await self.model.query(prompt, prompt_base)
        self.update_last_message(answer)


# singleton Player C
class GamePlayerC(GamePlayer):
    def __init__(self, username=basemodel_Imitation_Game.Prefixes.PlayerC.value):
        super(GamePlayerC, self).__init__(username)
        self.username = username
        self.model = None
        self.game_chat_id = None

    def setup_player(self, game_chat_id, model=None):
        self.model = model
        self.game_chat_id = game_chat_id

    async def form_question(self, player_a, player_b):
        prompt_base = prompt_base_question_player_c(
            player_a.username, player_b.username
        )
        prompt = prompt_question_player_c(dificulty="easy")
        question = await self.model.query(prompt, prompt_base)
        self.update_last_message(question)

    async def try2decide(self, player_a, player_b):
        prompt_base = prompt_base_full_desicion_player_c(
            player_a.username, player_b.username
        )
        prompt = prompt_full_desicion_player_c(player_a, player_b, self)
        logger.info(f"{self.game_chat_id} - try2decide ")
        text_decision = await self.model.query(prompt, prompt_base)
        logger.info(
            f"{self.game_chat_id} - try2decide " f"\n {prompt} \n {text_decision}"
        )
        reasoning = self.try_get_reasoning(text_decision)
        decision = await self.try_get_decision(
            text_decision, player_a.username, player_b.username
        )
        confidence = await self.try_get_confidence(
            text_decision, player_a.username, player_b.username
        )
        text_decision = self.form_full_decision_text(reasoning, decision, confidence)
        is_there_decision = True if confidence > 79 else False
        if is_there_decision:
            self.update_last_message(text_decision)
        return is_there_decision, text_decision

    async def try_get_confidence(
        self, text_decision, player_a_username, player_b_username
    ):
        async def _this():
            prompt_base = prompt_base_try_get_confidence_player_c(
                player_a_username, player_b_username
            )
            prompt = prompt_try_get_confidence_player_c(text_decision)
            logger.info(f"{self.game_chat_id} - try_get_confidence - attemp {i} ")
            new_text_decision = await self.model.query(prompt, prompt_base)
            logger.info(
                f"{self.game_chat_id} - try_get_confidence - attemp {i} "
                f"\n {prompt} \n {new_text_decision}"
            )
            return new_text_decision

        new_text_decision = text_decision
        confidence_metric = (
            basemodel_Imitation_Game.ChatIndicators.Confidence_Metric.value
        )
        confidence_metric_l = [
            confidence_metric,
            confidence_metric.lower(),
            "".join(confidence_metric.split(" ")),
            "".join(confidence_metric.lower().split(" ")),
        ]
        for i in range(3):
            for confidence_metric in confidence_metric_l:
                try_get_confidence = new_text_decision.split(confidence_metric)
                if len(try_get_confidence) > 1:
                    try:
                        try_get_confidence = re.findall(
                            r"[0-9]+", try_get_confidence[-1]
                        )[0]
                        confidence = int(try_get_confidence)
                        return confidence
                    except:
                        if any(cna in try_get_confidence for cna in ["N/A", "n/a"]):
                            return 50
                        break
            new_text_decision = await _this()
        return 0

    async def try_get_decision(
        self, text_decision, player_a_username, player_b_username
    ):
        new_text_decision = text_decision
        decision = basemodel_Imitation_Game.ChatIndicators.Decision.value
        confidence_metric = (
            basemodel_Imitation_Game.ChatIndicators.Confidence_Metric.value
        )
        to_return = f"{decision} : "
        for i in range(3):
            try_get_decision = new_text_decision.split(decision)
            if len(try_get_decision) > 1:
                try_get_decision = try_get_decision[-1]
                try_get_decision = try_get_decision.split(confidence_metric)[0]
                to_return += try_get_decision.strip()
                break
            else:
                prompt_base = prompt_base_try_get_decision_player_c(
                    player_a_username, player_b_username
                )
                prompt = prompt_try_get_decision_player_c(text_decision)
                logger.info(f"{self.game_chat_id} - try_get_decision - attemp {i} ")
                new_text_decision = await self.model.query(prompt, prompt_base)
                logger.info(
                    f"{self.game_chat_id} - try_get_decision - attemp {i} "
                    f"\n {prompt} \n {new_text_decision}"
                )
        return to_return.strip()

    def try_get_reasoning(self, text_decision):
        new_text_decision = text_decision
        reasoning = basemodel_Imitation_Game.ChatIndicators.Reasoning.value
        decision = basemodel_Imitation_Game.ChatIndicators.Decision.value
        confidence_metric = (
            basemodel_Imitation_Game.ChatIndicators.Confidence_Metric.value
        )
        to_return = f"{reasoning} : "
        try_get_reasoning = new_text_decision.split(reasoning)
        if len(try_get_reasoning) > 1:
            try_get_reasoning = try_get_reasoning[-1]
            try_get_reasoning = try_get_reasoning.split(decision)[0]
            try_get_reasoning = try_get_reasoning.split(confidence_metric)[0]
            to_return += try_get_reasoning.strip()
        else:
            logger.info(f"{self.game_chat_id} - try_get_reasoning")
            to_return += new_text_decision
        return to_return.strip()

    def form_full_decision_text(self, reasoning, decision, confidence):
        confidence_metric = (
            basemodel_Imitation_Game.ChatIndicators.Confidence_Metric.value
        )
        full_decision_text = ""
        full_decision_text += reasoning.strip() + "\n\n"
        full_decision_text += decision.strip() + "\n\n"
        full_decision_text += (
            confidence_metric + " : " + str(confidence).strip() + "\n\n"
        )
        return full_decision_text
