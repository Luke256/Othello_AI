from keras.models import Sequential
from keras.layers import Dense,Flatten,Reshape,Conv2D
from keras.optimizers import Adam,SGD

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

import numpy as np
import random
import copy
import sys
import datetime
import matplotlib.pyplot as plt

from Othello import Othello

env=Othello()
nb_actions = env.action_space.n

model=Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Reshape((8,8,1)))
model.add(Conv2D(filters=64,kernel_size=(3,3),activation="relu"))
model.add(Conv2D(filters=64,kernel_size=(3,3),activation="relu"))
model.add(Flatten())
model.add(Dense(units=128,activation="relu"))
model.add(Dense(units=128,activation="relu"))
model.add(Dense(units=nb_actions,activation="linear"))

model.summary()

memory=SequentialMemory(limit=10000,window_length=1)

policy=EpsGreedyQPolicy(eps=0.1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100, target_model_update=1e-2, policy=policy)
dqn.compile(SGD(),metrics=["acc"])

history=dqn.fit(env,nb_steps=60000,visualize=True,verbose=1,nb_max_episode_steps=64)
# dqn.test(env,nb_episodes=10)


num_ave=50
hist_ave=[]
hist_stack=0
for i, v in enumerate(history.history["nb_episode_steps"]):
    hist_stack += v
    if i >= num_ave-1:
        hist_ave.append(hist_stack / num_ave)
        hist_stack -= history.history["nb_episode_steps"][i - num_ave+1]
    else:
        hist_ave.append(hist_stack / (i+1))
        
plt.subplot(2,1,1)
plt.plot(history.history["nb_episode_steps"])
plt.plot(hist_ave)
plt.ylabel("step")


hist_ave=[]
hist_stack=0
for i, v in enumerate(history.history["episode_reward"]):
    hist_stack += v
    if i >= num_ave-1:
        hist_ave.append(hist_stack / num_ave)
        hist_stack -= history.history["episode_reward"][i - num_ave+1]
    else:
        hist_ave.append(hist_stack / (i+1))
plt.subplot(2,1,2)
plt.plot(history.history["episode_reward"])
plt.plot(hist_ave)
plt.xlabel("episode")
plt.ylabel("reward")

plt.grid()
plt.show()


json_string=dqn.model.to_json()
open('double conv.json', 'w').write(json_string)

# After training is done, we save the final weights.
dqn.save_weights('double conv.h5f5', overwrite=True)