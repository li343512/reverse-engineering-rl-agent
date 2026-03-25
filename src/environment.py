import gym

class BlackBoxEnvironment(gym.Env):
    def __init__(self):
        super(BlackBoxEnvironment, self).__init__()
        self.state = [0, 0, 1, False]  # Initial state
        self.action_space = gym.spaces.Discrete(4)  # 4 discrete actions
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(4,), dtype=int)  # 4-dimensional state within limits

    def step(self, action):
        if action == 0:
            self.state[0] += 1  # Increment state[0]
        elif action == 1:
            self.state[1] -= 1  # Decrement state[1]
        elif action == 2:
            self.state[2] = (self.state[2] * 2) % 256  # Multiply state[2] by 2 mod 256
        elif action == 3:
            self.state[3] = not self.state[3]  # Toggle state[3]

        reward = self.compute_reward()  # Compute reward after action
        done = False  # Define when to end the episode
        return self.state, reward, done, {}

    def compute_reward(self):
        reward = 0
        reward += self.state[0]  # Encourage maximizing state[0]
        reward -= self.state[1]  # Encourage minimizing state[1]
        if (self.state[2] & (self.state[2] - 1)) == 0:  # Check if state[2] is a power of 2
            reward += 10  # Extra reward for state[2] being a power of 2
        return reward

    def reset(self):
        self.state = [0, 0, 1, False]  # Reset state
        return self.state  # Return initial state

    def render(self, mode='human'):  # Optional rendering method
        pass  # Implement visualization if needed
