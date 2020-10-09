print("モージュールのインポート...")

from keras.models import Sequential
from keras.layers import Dense,Conv2D

import numpy as np
import random
import copy
import sys

from Othello import Othello

print("完了")


print("予測用ネットワーク構築...")
model_pre=Sequential()
model_pre.add(Dense(units=64,activation="relu",input_shape=(64,)))
model_pre.add(Dense(units=128,activation="relu"))
model_pre.add(Dense(units=64,activation="relu"))
model_pre.compile(optimizer="Adam",loss="mae",metrics=["accuary"])
# model_pre.summary()
print("完了")

print("行動決定用ネットワーク構築...")
model_act=Sequential()
model_act.add(Dense(units=64,activation="relu",input_shape=(128,)))
model_act.add(Dense(units=128,activation="relu"))
model_act.add(Dense(units=64,activation="softmax"))
model_act.compile(optimizer="Adam",loss="mae",metrics=["accuary"])
# model_act.summary()
print("完了")
print("エージェント初期化中...")

PRE_WEIGHT=np.array(model_pre.get_weights())
ACT_WEIGHT=np.array(model_act.get_weights())

Agents=[]
NUM_AGENT=10

for i in range(NUM_AGENT):
    tmp=[]
    
    #Pre
    pre=[]
    for i in range(PRE_WEIGHT.shape[0]):
        t0=[]
        if i%2==0:
            for j in range(PRE_WEIGHT[i].shape[0]):
                t1=[]
                for k in range(PRE_WEIGHT[i].shape[1]):
                    t1.append(random.random()*2-1.0)
                t0.append(t1)
        else:
            for j in range(PRE_WEIGHT[i].shape[0]):
                t0.append(random.random()*2-1.0)
        pre.append(np.array(t0))
    
    tmp.append(pre)
    
    #Act
    act=[]
    for i in range(ACT_WEIGHT.shape[0]):
        t0=[]
        if(i%2==0):
            for j in range(ACT_WEIGHT[i].shape[0]):
                t1=[]
                for k in range(ACT_WEIGHT[i].shape[1]):
                    t1.append(random.random()*2-1.0)
                t0.append(t1)
        else:
            for j in range(ACT_WEIGHT[i].shape[0]):
                t0.append(random.random()*2-1.0)
        act.append(np.array(t0))
    tmp.append(act)
    
    Agents.append(tmp)
print("完了")

print("学習用環境初期化中...")
env=Othello()
print("完了")

state=np.array(env.field)
state=np.reshape(state,(1,64,))
# print(state)
# print(state.shape)

for i in range(NUM_AGENT-1):
    for j in range(i+1):
        env.reset()
        while(not env.finish):
            env.turn=2
            if env.turn==1:
                model_pre.set_weights(Agents[i][0])
                model_act.set_weights(Agents[i][1])
                state=np.array(env.field)
                state=np.reshape(state,(1,64))

                result_pre=model_pre.predict(state)
            else:
                state=copy.deepcopy(env.field[0:][-1::-1])
                for i_k,k in enumerate(state):
                    for i_l,l in enumerate(k):
                        if(l!=0):
                            state[i_k][i_l]=3-l
                state=np.array(state)
                state=np.reshape(state,(1,64))