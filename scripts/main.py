import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

from scripts.config import *
from scripts.utils import *
from scripts.agent import *

from time import sleep

# Load Settings & variables from config
env_settings, wrappers_settings = json_to_py_start()

# Instance Env
env, _ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)


is_server=False
# Instance Agent
if is_server:
    # WIP : when 3client : n_steps => 3 x n_steps
    server = AgentServer(env, n_steps=n_steps)

else:
    client = AgentClient(env, n_steps=n_steps)


# LOOP
i = 0
while i < looping:
    i += 1

    if is_server: server.run()

    else:
        client.run()
