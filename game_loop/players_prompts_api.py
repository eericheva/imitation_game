def prompt_base_player_c(player_a_username, player_b_username):
    prompt = (
        "You are a judge in an Imitation Game where you need to determine who is the human and who is the robot "
        f"between {player_a_username} and {player_b_username}. "
        "To make this decision, you will ask both players a series of questions and analyze their responses."
        "After evaluating their answers, you will provide a detailed reasoning for "
        "your decision and a confidence metric (from 0 to 100) indicating how certain you are of your judgment. "
        "If you are unsure, provide a lower confidence number. \n"
    )
    return prompt


def prompt_question_player_c(player_a_username, player_b_username, dificulty="easy"):
    prompt = prompt_base_player_c(player_a_username, player_b_username)
    prompt += (
        "Example of your question: \n"
        "Question: Describe a personal experience or memory that had a significant impact on your life. \n"
    )
    prompt += f"Now ask me a {dificulty} question. Provide only 1 question."
    prompt += "Question: "
    return prompt


def prompt_desicion_player_c(player_a, player_b, player_c):
    prompt = prompt_base_player_c(player_a.username, player_b.username)
    prompt += (
        "Your Task:"
        f"1. Analyze the responses from both {player_a.username} and {player_a.username}. \n"
        "2. Based on the nuances in their answers, such as the presence of personal anecdotes, "
        "emotional depth, and complexity of thought, decide which player is more likely to be human \n"
        "3. Provide a detailed explanation of your reasoning. \n"
        "4. Assign a confidence metric (0 to 100) indicating how certain you are of your decision. \n"
        "5. If you are not very sure, provide a lower confidence number.\n"
    )
    prompt += (
        "Example of your return : Reasoning and Confidence Metric:"
        f" Reasoning: {player_a.username}’s responses included detailed personal experiences and "
        "demonstrated a deep understanding of emotional nuances, which are challenging for AI to "
        f"mimic accurately. \n"
        f"{player_b.username}’s answers were more factual and lacked the same level of personal "
        "detail and emotional depth. \n"
        " Confidence Metric: 85 \n\n"
    )
    prompt += "Here are their history of responses: \n"
    for i, question in enumerate(player_c.user_history):
        prompt += "\n"
        prompt += f"Question : {question} \n"
        prompt += f"{player_a.user_history[i]} \n"
        prompt += f"{player_b.user_history[i]} \n"
    prompt += (
        " Now, based on the responses from their history of responses below, provide your "
        "reasoning and confidence metric to determine who is the human and who is the robot."
    )
    return prompt


def prompt_answer_player_b(input_text):
    prompt = f"Answer this question in 3 sentences: {input_text}"
    return prompt
