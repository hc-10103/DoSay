import gymnasium as gym
import numpy as np


class ClipReward(gym.RewardWrapper):
    def __init__(self, env, min_reward, max_reward):
        super().__init__(env)
        self.min_reward = min_reward
        self.max_reward = max_reward
        self.reward_range = (min_reward, max_reward)

    def reward(self, reward):
        reward = (float)(reward)
        minR = (float)(self.min_reward)
        maxR = (float)(self.max_reward)
        return np.clip(reward, minR, maxR)