import random
import sqlite3
import os
import statistics
import sys

import pandas as pd
import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pickle
import copy
from heapq import heappush, heappop, nsmallest
from tqdm import tqdm

from matplotlib import animation
from data.utils import create_graph
from data.utils import import_requests_from_csv
from data.utils import Driver
from data.utils import choose_random_node


class TopEnvironment:
    FREE = 0
    OCCUPIED = 1

    def __init__(self, gamma, drivers_num, speed=5000., start_time=None, timestep=1, final_time=50,
                 fairness_discount=0.9):
        # 新增变量和初始化
        self.agent_num = drivers_num
        self.obs_dim = 4
        self.action_dim = 100
        self.train_days = [39]
        self.drivers = []
        for i in range(self.agent_num):
            self.drivers.append(Driver(0))
        for idx, driver in enumerate(self.drivers):
            driver.on_road = 0
            driver.idx = idx
            driver.money = 0
            driver.speed = 5000
        self.start_time = start_time
        self.timestep = timestep
        self.final_time = final_time
        self.time = 0
        self.done = False
        self.graph = create_graph()
        self.all_requests = import_requests_from_csv()
        self.requests = []

    def _generate_observation(self):
        state = np.zeros((self.agent_num, self.obs_dim))
        for i, driver in enumerate(self.drivers):
            state[i, 0] = 1 if driver.on_road == self.FREE else 0
            state[i, 1] = driver.pos
            state[i, 2] = self.time  # 填充更多司机相关信息
            state[i, 3] = driver.money  # 假设只填充4个维度

        return state

    def reset(self):
        for driver in self.drivers:
            driver.on_road = self.FREE
            driver.money = 0
            driver.pos = np.random.randint(0, 100)  # 随机选择一个位置

        self.time = 0
        self.requests = []
        self.requests.extend(self.all_requests[0])
        self.done = False
        return self._generate_observation()

    def step(self, action):
        for driver in self.drivers:
            if driver.on_road == 1:
                driver.start_time += self.timestep
                if (self.graph.get_edge_data(driver.Request.origin, driver.Request.destination)["distance"] -
                    self.graph.get_edge_data(driver.pos,
                                             driver.Request.origin)[
                        "distance"]) / driver.speed <= driver.start_time:
                    driver.on_road = 0
                    driver.pos = driver.Request.destination
                    driver.money += self.graph.get_edge_data(driver.Request.origin,
                                                             driver.Request.destination)["distance"]
        sorted_drivers = sorted(self.drivers, key=lambda d: d.money)
        # sort 目的地
        reward_list = []
        end_list = []
        for idx, driver in enumerate(sorted_drivers):
            actions = []
            # 选出来的点
            actions.append(action[idx])
            actions.append(driver.idx)
            _,single_reward,done,_=self.single_step(actions)
            reward_list.append(single_reward)
            end_list.append(done)

        print("money is ")
        print(reward_list)

        self.time += self.timestep


        return self._state(), reward_list,end_list , {}

    def single_step(self, action):
        # action把他变成司机->request的形式传入step
        action_map = {}
        select_actions = []
        reward = 0
        if self.drivers[action[1]].on_road == 0:
            action_onehot=action[0]
            node_idx = action_onehot.tolist().index(1)
            print(node_idx)
            for r in self.requests:
                if (r.destination == node_idx) & (r.state == 0):
                    select_actions.append(r)
            if len(select_actions) != 0:
                random_action = random.choice(select_actions)
                random_action.state = 1
                reward = (self.graph.get_edge_data(random_action.origin, random_action.destination)["distance"] -
                          self.graph.get_edge_data(self.drivers[action[1]].pos,
                                                   random_action.origin)["distance"])
                self.drivers[action[1]].on_road = 1
                self.drivers[action[1]].Request = random_action
        if self.time >= self.final_time:
            self.done = True
        return self._state(), reward, self.done, {}

    def _state(self):
        return self._generate_observation()

    # def test(self):
    #     print("Testing environment with {} agents".format(self.agent_num))
    #     obs = self.reset()
    #     print("Initial observations:", obs)
    #
    #     # 随机生成并执行动作
    #     actions = [np.random.randint(self.action_dim) for _ in range(self.agent_num)]
    #     print("Actions:", actions)
    #
    #     next_obs, rewards, done, _ = self.step(actions)
    #     print("Next observations:", next_obs)
    #     print("Rewards:", rewards)
    #     print("Done:", done)

# 测试环境
# gamma = 0.99  # 举例用的 gamma 值
# env = TopEnvironment(gamma)
# env.test()
