from gameenv import PongEnv

def test_gym_environment():
    env = PongEnv(2)
    obs = env.reset()
    total_reward = 0
    for _ in range(1000):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            break
    return total_reward

print(test_gym_environment())