# imitation_game

@AI_Imitation_Game_Bot

Hello!

**What is going on here:**

Here are three players. **Player A** is you, **Player B** is the invited AI bot, and **Player C** is me, the AI bot
acting as the conversation host. According to the rules of the game, I don't know which of **Players A** and **B** is
the bot and which is the human, and I can only communicate with you through written messages. By asking questions to
**Players A** and **B**, I will try to determine who is the bot and who is the human.

Your task is to confuse me, pretending to be the bot (or a human) so that I make the wrong conclusion. At the same time,
the Player B's (bot) task is to help me make the correct judgment and correctly identify which player is the human.

Wanna play?

**There are two game modes possible**

- **Blind** means - Player A (you) cannot see Player B's answers or Player C's reasoning about how they make decisions
  after each answer.
- **Explanatory** means - before Player A is given the opportunity to answer, they will see Player B's response. After
  each series of questions and answers, Player C's reasoning for making their decision will be shown.

**There are two types of imitation games possible**

- **Direct** imitation game - Player A and Player B both pretend to be humans.
- **Inverse** imitation game - both players pretend to be bots.

## Some technical backend realization details:

### Deployment with Heroku

**Free and simple**

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

Files:

- [runtime.txt](ig_app/runtime.txt)
- [Procfile](ig_app/Procfile)

Github Actions:

- [.github/workflows/deploy_heroku.yml](.github/workflows/deploy_heroku.yml)

### Deployment with Docker:

**Example with run llama.cpp.server**

Main proccess run and serve telegram bot. Llama.ccp server run and serve llm generation.

Files:

- [ig_app/Dockerfile](ig_app/Dockerfile) - Dockerfile for main proccess (
  uses [ig_app/requirements.txt](ig_app/requirements.txt))
- [llama_cpp_server/Dockerfile](llama_cpp_server/Dockerfile) - Dockerfile for llama.cpp server (
  uses [llama_cpp_server/requirements.txt](llama_cpp_server/requirements.txt)
  and [llama_cpp_server/llama_cpp_server_config.json](llama_cpp_server/llama_cpp_server_config.json))
- Build local [docker-compose.yml](docker-compose.yml)
- Run local [docker_push_and_run.sh](docker_push_and_run.sh)
```
chmod +x docker_push_and_run.sh
./docker_push_and_run.sh
  ```

Github Action:

- [.github/workflows/deploy_docker.yml](.github/workflows/deploy_docker.yml)

### Run through HuggingFace API inference

Quick start to API interface : https://huggingface.co/inference-api/serverless

Detailed payload parameters for different task types: https://huggingface.co/docs/api-inference/detailed_parameters

example [game_loop/players_models_api.py](ig_app/game_loop/players_models_api.py)

### Run through HuggingFace local:

example [game_loop/players_models_hf.py](ig_app/game_loop/players_models_hf.py)

### Run through local Transformers with Quantization:

**Cool for save disk space, RAM and speed generation**

`pip install accelerate` - for device_map="auto"

`pip install optimum, auto-gptq` - for GPTQQuantizer

```
pip install intel-extension-for-pytorch==2.2
# intel-extension-for-pytorch==2.2 requires
# transformers==4.35.2
# torch==2.2.*
```

source lib [intel-extension-for-pytorch](https://github.com/intel/intel-extension-for-pytorch)

example [game_loop/players_models_woq.py](ig_app/game_loop/players_models_woq.py)

### Run through LLama-cpp-python

**Cool for extremelly fast model generation**

```
pip install llama_cpp_python
```

LLama.cpp
source [llama-cpp-python/high-level-api](https://github.com/abetlen/llama-cpp-python/tree/main?tab=readme-ov-file#high-level-api)

Quick start to llama-cpp-python package : https://llama-cpp-python.readthedocs.io/en/latest/

example [game_loop/players_models_llamacpp.py](ig_app/game_loop/players_models_llamacpp.py)

### Run through LLama.cpp Sever and OpenAI API (async):

**Cool for async llm calls**

```
pip install openai
pip install 'llama-cpp-python[server]'
python -m llama_cpp.server --model models/7B/llama-model.gguf
```

OpenAI API source [openai-python](https://github.com/openai/openai-python)

LLama.cpp Server
source [llama-cpp-python/openai-compatible-web-server](https://github.com/abetlen/llama-cpp-python/tree/main?tab=readme-ov-file#openai-compatible-web-server)

To avoid `warning: failed to munlock buffer: Cannot allocate memory` run with

```
ulimit -l unlimited && python -m llama_cpp.server --config_file <config_file>
```

config_file example [llama_cpp_server_covfig.json](llama_cpp_server/llama_cpp_server_config.json)

example [game_loop/players_models_openai.py](ig_app/game_loop/players_models_openai.py)

## Some technical ML realisation details:

Players C's decisions provided with **text-generation** task LLM.

LLM-GGUF to use here : second-state/Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf

### todo:

- Players C's decisions provided with **embeddings-classification** task LLM.
- Add other LLMs for comparing
