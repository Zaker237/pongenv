import click
import os
from pathlib import Path
from stable_baselines3.ppo import MlpPolicy, PPO
from stable_baselines3.common.wrappers import ActionMasker
from stable_baselines3.common.callbacks import EvalCallback

from gameenv import RandomAgent, PongEnv

TENSORDIR = (Path("./models")/ Path("ppo_tensorboard")).absolute()
LOGDIR = (Path("./models")/Path("ppo_eval")).absolute()

SEED = 416

NUM_TIMESTEPS = 1e7
EVAL_FREQ = 5000
EVAL_EPISODES = 100


@click.command()
@click.option("--load_path", "-l", type=click.Path(), type=int, default="models")
@click.option("--num_players", "-np", type=int, default=2)
def train(load_path, num_players):
    env = PongEnv(num_players)
    env.seed(SEED)
    #env = ActionMasker(env, 'valid_actions')

    model = PPO(MlpPolicy, env, verbose=1, tensorboard_log=LOGDIR) #, action_mask_fn='valid_actions')
    if load_path:
        model.load(Path(load_path).absolute())

    random_agents = [RandomAgent(env, i + 1, SEED + i) for i in range(num_players - 1)]
    agents = [model, *random_agents]
    env.set_agents(agents)

    eval_callback = EvalCallback(env, best_model_save_path=LOGDIR, log_path=LOGDIR,
                                 eval_freq=EVAL_FREQ, n_eval_episodes=EVAL_EPISODES)

    model.learn(total_timesteps=NUM_TIMESTEPS, callback=eval_callback, tb_log_name='PPO_GCS_1')

    model.save((Path("./models")/Path("final_ppo_model")).absolute())

    env.close()


if __name__ == "__main__":
    train()