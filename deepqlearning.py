import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense

import gym
import pygame
import gym_maze

class sarsa():
  def __init__(self, env, network, learning_rate=0.02, gamma=0.99):
    self.env = env
    self.network = network
    self.loss_object = tf.keras.losses.MeanSquaredError()
    self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    self.train_loss = tf.keras.metrics.Mean(name='train_loss')


    self.gamma = gamma
    self.nA = env.action_space.n 

  # recebe a predição da rede e converte numa e-greedy policy
  def get_greedy(eps, prediction):
    greedy = np.ones(self.nA)*eps/self.nA
    a_max = np.argmax(prediction)
    greedy[a_max] = 1 - eps + eps/self.nA
    return greedy

  @tf.function
  def train(self, state, eps):
    with tf.GradientTape() as tape:
      predictions = self.network(state, training=True)
      act = np.random.choice(self.nA, 1, p=predictions)[0]
      next_state, reward, done, _ = self.env.step(act)

      next_predictions = self.network(next_state, training=True)
      next_policy = self.get_greedy(eps, next_predictions)
      next_act = np.random.choice(self.nA, 1, p=next_policy)[0]
      td_target = reward + self.gamma*next_predictions[next_act]
      loss = loss_object(predictions, td_target)
    gradients = tape.gradients(loss, model.trainable_variables)
    self.optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    self.train_loss(loss)
    if done:
      return True
    return False
  
  # o agente apenas joga, não aprende. eh retornada a ação escolhida
  @tf.function
  def test(self, state, eps):
    predictions = self.network(state, training=False)
    return np.random.choice(self.nA, 1, p=predictions)[0]

env = gym.make('maze-random-10x10-v0')

nS = env.observation_space.n
nA = env.action_space.n

net = tf.keras.models.Sequential([Dense(4, activation='relu', input_shape=(1,)),
                                  Dense(nA, activation='softmax')])

net.summary()

agent = sarsa(env, net)

n_episodes = 50
eps = 1.0
for n in range(1, n_episodes + 1):
  state = env.reset()
  while(1):
    state = tf.convert_to_tensor(state)
    print(state)
    state = tf.expand_dims(state, 1)

    print(state)
    done = agent.train(state, eps)
    if done:
      break
  eps = 1/n

