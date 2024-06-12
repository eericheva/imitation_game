# imitation_game

Hello!

**What is going on here:**

Here are three players. **Player A** is you, **Player B** is the invited AI bot, and **Player C** is me, the AI bot
acting as the conversation host. According to the rules of the game, I don't know which of **Players A** and **B** is
the bot and which is the human, and I can only communicate with you through written messages. By asking questions to **
Players A** and **B**, I will try to determine who is the bot and who is the human.

Your task is to confuse me, pretending to be the bot so that I make the wrong conclusion. At the same time, the invited
AI bot's task is to help me make the correct judgment and correctly identify which player is the human.

Wanna play?

**In which mode will we play?**

**Blind** means - Player A (you) cannot see Player B's answers or Player C's reasoning about how they make decisions
after each answer.

**Explanatory** means - before Player A is given the opportunity to answer, they will see Player B's response. After
each series of questions and answers, Player C's reasoning for making their decision will be shown.

### Some technical realisation details:

All are free and simple

### Deployment with Heroku

To deploy such a model on a free deployment website, it is important to keep everything as small as possible. Do not
upload cache or virtual environment files to the deployment, and make sure you only use parts of packages that you need.
The Pytorch package made my app exceed the allowed ‘slug’ limit of 500MB on Heroku. By only downloading the CPU version,
we saved roughly 300–400MB of space.

Update _requirements.txt_ file:

- add to _requirements.txt_ file `-f https://download.pytorch.org/whl/torch_stable.html`
- run in console
  `pip install torch== -f https://download.pytorch.org/whl/torch_stable.html`
- find in the output error available `+cpu` torch version
- add it to _requirements.txt_ file: (example: `torch==1.11.0+cpu`)

Github Actions:

- [deploy_heroku.yml](.github/workflows/deploy_heroku.yml)

### Run through HuggingFace API inference

Quick start to API interface : https://huggingface.co/inference-api/serverless

Detailed payload parameters for different task types: https://huggingface.co/docs/api-inference/detailed_parameters

### Run through LLama.cpp

Quick start to llama-cpp-python package : https://llama-cpp-python.readthedocs.io/en/latest/

### Run through local Transformers

`pip install accelerate` - for device_map="auto"

`pip install optimum, auto-gptq` - for GPTQQuantizer
