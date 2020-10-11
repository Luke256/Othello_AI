import random
import numpy as np
import gym
import gym.spaces
import pygame
from pygame.locals import *

class Othello(gym.core.Env):


    """
    0:None
    1:Black
    2:White
    """
    def __init__(self):
        pygame.init()
        self.dis = pygame.display.set_mode((400, 400))
        
        self.field=[
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]

        self.turn=1
        self.finish=False
        self.Pass=False
        self.white=2
        self.black=2
        
        self.action_space = gym.spaces.Discrete(64)
        low=[]
        for i in range(64):
            low.append(0)
        low=np.array(low)
        high=[]
        for i in range(64):
            high.append(2)
        high=np.array(high)
        
        self.observation_space = gym.spaces.Box(low=low, high=high)
        
        return 

    def step(self,act):
        reward=0
        wrong=False
        #盤面更新
        ok=self.isOK(act)
        if ok:
            self.isOK(act,True)
            # for i in self.field:
            #     print(i)
            reward+=1
        else:
            # print("You can't put on {}".format(act))
            reward-=3
            wrong=True
            
            
        if not wrong:
            #ランダムに置く
            self.turn=3-self.turn
            r=random.randrange(0,64)
            while(not self.isOK(r)):
                r=random.randrange(0,64)
            self.isOK(r,True)
            self.turn=3-self.turn
            
        #石を数える
        self.black=self.white=0
        for i in self.field:
            for j in i:
                if j==1:
                    self.black+=1
                if j==2:
                    self.white+=1

        #終了判定・置ける場所の計測
        able_put=[0,0] #white black (2-0=2,2-1=1)
        f=True
        self.Pass=True
        for index_i,i in enumerate(self.field):
            for index_j,j in enumerate(i):
                if self.isOK(index_i*8+index_j):
                    f=False
                    self.Pass=False
                    able_put[2-self.turn]+=1
                self.turn=3-self.turn
                if self.isOK(index_i*8+index_j):
                    f=False
                    able_put[2-self.turn]+=1
                self.turn=3-self.turn
                
                if j==1 and (index_i==0 or index_i==7 or index_j==0 or index_j==7): #端は得点高め
                    reward+=0.05
                    if(index_i==0 or index_i==7 )and( index_j==0 or index_j==7):
                        reward+=0.15
            
        self.finish=f
        
        #報酬計算
        try:
            if self.turn==1:
                reward+=(self.black/self.white)#+(able_put[1]/able_put[0])
            else:
                reward+=(self.white/self.black)#+(able_put[0]/able_put[1])
        except ZeroDivisionError:
            if self.turn==1:
                reward+=(able_put[1])+(self.black)
            else:
                reward+=(able_put[0])+(self.white)
        
        reward/=64
                
        if wrong:
            reward=-1
            self.finish=True
                
        state=np.array(self.field)
        state=np.reshape(state,(64))
                
            
        return state,reward,self.finish,{}

    def reset(self):
        self.field=[
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]

        self.turn=1
        self.finish=False
        self.Pass=False
        self.white=2
        self.black=2
        state=np.array(self.field)
        state=np.reshape(state,(64))
        return state
    
    def render(self, mode="human", close=False):
        self.dis.fill((255,255,255))
        pygame.draw.rect(self.dis,(0,255,0),Rect(40,40,320,320))
        for index_i,i in enumerate(self.field):
            for index_j,j in enumerate(i):
                if j==1:
                    pygame.draw.circle(self.dis,(0,0,0),(60+index_j*40,60+index_i*40),15)
                elif j==2:
                    pygame.draw.circle(self.dis,(255,255,255),(60+index_j*40,60+index_i*40),15)
        pygame.display.update()


    def isOK(self,act,shift=False):
        vec=[-1,0,1]
        ok=False
        
        if(self.field[act//8][act%8]!=0):
            return False

        for i in vec:
            for j in vec:
                if i==0 and j==0:
                    continue
                if(self.isOK_sub(act,i,j,shift)):
                    ok=True

        return ok

    def isOK_sub(self,act,i,j,shift,req=False):
        n_i=act//8
        n_j=act%8
        next=(n_i+i)*8+n_j+j

        if not (0<=n_i+i<8 and 0<=n_j+j<8):
            return False

        if self.field[n_i+i][n_j+j]==3-self.turn:
            result=self.isOK_sub(next,i,j,shift,req=True)
            if result and shift:
                self.field[n_i][n_j]=self.turn
            return result
        elif self.field[n_i+i][n_j+j]==0:
            return False
        else:
            if req:
                if shift:
                    self.field[n_i][n_j]=self.turn
                return True
            else:
                return False


if __name__=="__main__":
    a=Othello()
    for i in a.field:
        print(i)
        
    for i in range(64):
        a.step(i)