import numpy as np

#

class EnvCore(object):
    def __init__(self, agent_num, T, MaxNum):
        self.agent_num = agent_num
        self.T = T
        self.MaxNum = MaxNum
        self.current_time = 0
        self.state_space = np.zeros((agent_num, 4))  #状态矩阵: [availability, position, timestep, cumulative_reward]

    def reset(self):
        self.current_time = 0
        self.state_space[:, 0] = 1
        self.state_space[:, 1] = np.random.randint(0, self.MaxNum, size=(self.agent_num,))
        self.state_space[:, 2] = 0
        self.state_space[:, 3] = 0
        return self.state_space

    def step(self, actions, strategy="priority_order"):
        rewards = np.zeros(self.agent_num)
        dones = np.array([self.current_time >= self.T] * self.agent_num)
        infos = [{} for _ in range(self.agent_num)]

        # Call the strategy method based on the strategy argument
        if strategy == "priority_order":
            self.apply_action_priority_order(actions)
        elif strategy == "random_order":
            self.apply_action_random_order(actions)

        self.current_time += 1  # Increment the timestep
        return self.state_space, rewards, dones, infos

    def apply_action_priority_order(self, actions):
        for action in actions:
            for i, agent_state in enumerate(self.state_space):
                if self.current_time == action[0] and agent_state[0] == 1:
                    self.state_space[i, 0] = 0
                    self.state_space[i, 1] = action[1]
                    self.state_space[i, 2] = action[2]
                    self.state_space[i, 3] += action[3]
                    break

    def apply_action_random_order(self, actions):
        available_agents = [i for i, agent_state in enumerate(self.state_space) if agent_state[0] == 1]
        np.random.shuffle(available_agents)

        for action in actions:
            for i in available_agents:
                if self.current_time == action[0]:
                    self.state_space[i, 0] = 0
                    self.state_space[i, 1] = action[1]
                    self.state_space[i, 2] = action[2]
                    self.state_space[i, 3] += action[3]
                    available_agents.remove(i)
                    break

env_core = EnvCore(agent_num=5, T=10, MaxNum=15)

initial_states = env_core.reset()
print('Initial states:', initial_states)

actions = [[0, 1, 3, 10], [0, 2, 3, 8], [0, 3, 3, 6], [0, 4, 3, 4], [0, 1, 3, 10]]
for _ in range(12):
    state, rewards, dones, infos = env_core.step(actions)
    print('State:', state, 'Rewards:', rewards, 'Dones:', dones)