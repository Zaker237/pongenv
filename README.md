# A reinforcement learning environment for the game Pong

In the repos, i provide An Environement for the game Pong. The Environement is based on OpenAI gym and can be trained with any RL approach.

# Developer Guide #

Then Environement is designed with python 3.7 in mind. How an environment can be created, how to train and evaluate models and how to modify the environment is discussed below.

## How to set up the Environment. ##

```s
python3 -m venv game-env
source game-env/bin/activate
pip3 install -r requirements.txt
```

The game is already implemented, nor yet perfect but work.

## How to play malually

The game can be play using the keyboard. The player at the top can move using **a** and **d**. The at the bottom moves using KEY right and Key left. The game can be lauch using the following command.

```s
python3 play.py
```


# Todo


- [ ] implement the environment
- [ ] optimize the collision check
- [ ] write docstring for methods and classes
- [ ] write the tests for the game
- [ ] write the tests for the environement



# How to contribute