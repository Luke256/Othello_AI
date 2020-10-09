print("モージュールのインポート...")

from keras.models import Sequential
from keras.layers import Dense,Conv2D

import numpy as np
import random
import copy
import sys
import datetime

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
NUM_AGENT=20

for index in range(NUM_AGENT):
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

# print(state)
# print(state.shape)


for epoch in range(150):
    print("**********")
    print("epoch:{}".format(epoch))
    print("**********")
    rewards=[[0,0,i] for i in range(NUM_AGENT)] #pre,act,index
    for i in range(NUM_AGENT-1):
        for j in range(i+1):
            print()
            env.reset()
            print("{} vs {} start".format(i,j))
            while(not env.finish):

                state=np.array(env.field)
                state=np.reshape(state,(1,64))

                if env.turn==1:
                    model_pre.set_weights(Agents[i+1][0])
                    model_act.set_weights(Agents[i+1][1])

                    result_pre=model_pre.predict(state)
                    state=np.concatenate([state,result_pre])
                    state=np.reshape(state,(1,128))
                    # print(state)
                    result_act=model_act.predict(state)
                    # print(result_act)
                    act=np.argmax(result_act[0])
                    # print(act)
                    if(not env.isOK(act)):
                        break
                    env.step(act)

                else:
                    state=copy.deepcopy(env.field[0:][-1::-1])
                    for i_k,k in enumerate(state):
                        for i_l,l in enumerate(k):
                            if(l!=0):
                                state[i_k][i_l]=3-l
                    state=np.array(state)
                    state=np.reshape(state,(1,64))


                    model_pre.set_weights(Agents[j][0])
                    model_act.set_weights(Agents[j][1])

                    result_pre=model_pre.predict(state)
                    state=np.concatenate([state,result_pre])
                    state=np.reshape(state,(1,128))
                    # print(state)
                    result_act=model_act.predict(state)
                    # print(result_act)
                    act=np.argmax(result_act[0])
                    # print(act)
                    if(not env.isOK(act)):
                        break
                    env.step(act)
                    
            num_i=0
            num_j=0
            for k in env.field:
                for l in k:
                    if l==1:
                        num_i+=1
                    elif l==2:
                        num_j+=1

            if(num_i<num_j):
                rewards[j][1]+=2
                if(num_i==0):
                    rewards[j][1]+=64
                else:
                    rewards[j][1]+=num_j//num_i
            elif(num_i>num_j):
                rewards[i+1][1]+=2
                if(num_j==0):
                    rewards[i][1]+=64
                else:
                    rewards[i][1]+=num_i//num_j
            else:
                rewards[i+1][1]+=1
                rewards[j][1]+=1
                
    result=np.array(sorted(rewards,key=lambda x: x[1])[-1::-1])
    print(result)
    parent=[copy.deepcopy(Agents[result[0][2]]),copy.deepcopy(Agents[result[1][2]])]
    print(parent[0][1][0][0])
    # sys.exit()
    
    Agents[0]=parent[0]
    Agents[1]=parent[1]
    
    for index in range(NUM_AGENT-2):
        tmp=[]

        #Pre
        pre=[]
        for i in range(PRE_WEIGHT.shape[0]):
            t0=[]
            if i%2==0:
                for j in range(PRE_WEIGHT[i].shape[0]):
                    t1=[]
                    for k in range(PRE_WEIGHT[i].shape[1]):
                        if random.random()>0.05:
                            t1.append(parent[random.randrange(0,2)][0][i][j][k])
                        else:
                            t1.append(random.random()*2-1)
                    t0.append(t1)
            else:
                for j in range(PRE_WEIGHT[i].shape[0]):
                    if random.random()>0.05:
                        t0.append(parent[random.randrange(0,2)][0][i][j])
                    else:
                        t0.append(random.random()*2-1)
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
                        if random.random()>0.05:
                            t1.append(parent[random.randrange(0,2)][1][i][j][k])
                        else:
                            t1.append(random.random()*2-1)
                    t0.append(t1)
            else:
                for j in range(ACT_WEIGHT[i].shape[0]):
                    if random.random()>0.05:
                        t0.append(parent[random.randrange(0,2)][1][i][j])
                    else:
                        t0.append(random.random()*2-1)
            act.append(np.array(t0))
        tmp.append(act)

        Agents[index+2]=tmp

model_pre.set_weights(Agents[0][0])
model_act.set_weights(Agents[0][1])


time=datetime.datetime.now()
json_string=model_pre.to_json()
open('test_pre {}.json'.format(time), 'w').write(json_string)
model_pre.save_weights('test_pre {}.h5f5'.format(time), overwrite=True)
json_string=model_act.to_json()
open('test_act {}.json'.format(time), 'w').write(json_string)
model_act.save_weights('test_act {}.h5f5'.format(time), overwrite=True)
