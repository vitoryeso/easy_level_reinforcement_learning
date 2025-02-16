import numpy as np
import gym
import gym_maze
import matplotlib.pyplot as plt
from time import sleep


from collections import defaultdict

class MC_agent:
    def __init__(self, env, gamma, alpha, start_eps, eps_step):
        self.env = env
        self.gamma = gamma
        self.alpha = alpha
        self.eps = start_eps
        self.eps_step = eps_step

        self.maze_act = ['N', 'S', 'W', 'E']
        self.nA = env.action_space.n
        self.Q = defaultdict(lambda: np.zeros(self.nA))
    
    def e_greedy(self, s, eps):
        policy = (np.ones(self.nA)*eps)/self.nA
        a_max = np.argmax(self.Q[s])
        policy[a_max] = 1 - eps + eps/self.nA
        return policy
    
    def play_episode(self, show=False, delay=1):
        episode = []
        state = tuple(self.env.reset())
        while(1):
            if show:
                sleep(delay)
                self.env.render()
            act = np.random.choice(4, 1, p=self.e_greedy(state, self.eps))[0]
            next_state, reward, done, _ = self.env.step(self.maze_act[act])
            next_state = tuple(next_state)
            episode.append((state, act, reward))
            state = next_state
            if done:
                break
        return episode

    def sum_rewards(self, rewards, i):
        soma = 0
        for n, j in enumerate(range(i, len(rewards))):
            soma += rewards[j] * (self.gamma**n)
        return soma

    def update_knowledge(self, episode, mode='first'):
        states, actions, rewards = zip(*episode)
        SA_pair = tuple(zip(states, actions))
        if mode == 'first':
            visited = []
            for i in range(len(SA_pair)):
                if SA_pair[i] not in visited:
                    state = SA_pair[i][0]
                    act = SA_pair[i][1]
                    self.Q[state][act] += self.alpha*(self.sum_rewards(rewards, i) - self.Q[state][act])
                    visited.append(SA_pair[i])
        if mode == 'every':
            for i in range(len(SA_pair)):
                if SA_pair[i] not in visited:
                    state = SA_pair[i][0]
                    act = SA_pair[i][1]
                    self.Q[state][act] += self.alpha*(self.sum_rewards(rewards, i) - self.Q[state][act])



