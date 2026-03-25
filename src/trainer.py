import numpy as np
from collections import deque
import matplotlib.pyplot as plt

class Trainer:
    def __init__(self, agent, env):
        self.agent = agent
        self.env = env
        self.episodes = []
        self.rewards = []

    def train(self, episodes=500, batch_size=32):
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            done = False
            while not done:
                action = self.agent.act(state)
                next_state, reward, done, _ = self.env.step(action)
                self.agent.remember(state, action, reward, next_state, done)
                if len(self.agent.memory) > batch_size:
                    self.agent.replay(batch_size)
                total_reward += reward
                state = next_state
            self.agent.epsilon_decay()
            self.episodes.append(episode)
            self.rewards.append(total_reward)
            if (episode + 1) % 50 == 0:
                avg_reward = np.mean(self.rewards[-50:])
                print(f"Episode: {episode + 1}/{episodes}, Average Reward: {avg_reward:.2f}")

    def evaluate(self, episodes=10):
        total_rewards = []
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            done = False
            while not done:
                action = self.agent.act(state)
                next_state, reward, done, _ = self.env.step(action)
                total_reward += reward
                state = next_state
        total_rewards.append(total_reward)
        avg_reward = np.mean(total_rewards)
        print(f"Evaluation - Average Reward: {avg_reward:.2f}")
        return avg_reward

    def plot_performance(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.episodes, self.rewards)
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.title('Training Performance')
        plt.savefig('training_performance.png')
        print("Plot saved to training_performance.png")
