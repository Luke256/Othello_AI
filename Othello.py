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
            high.append(3)
        high=np.array(high)
        
        self.observation_space = gym.spaces.Box(low=low, high=high)
        
        return 

    def step(self,act):
        reward=0
        wrong=False
        info = {}
        #盤面更新
        ok=self.isOK(act)
        if ok:
            self.isOK(act,True)
            # for i in self.field:
            #     print(i)
            reward+=1
        else:
            # print("You can't put on {}".format(act))
            wrong=True
            
        t=False
        
        self.turn=3-self.turn
        for index_i,i in enumerate(self.field):
            for index_j,j in enumerate(i):
                if self.isOK(index_i*8+index_j):
                    t=True
        self.turn=3-self.turn
            
        if (not wrong):
            #ランダムに置く
            while(t):
                self.turn=3-self.turn
                r=random.randrange(0,64)
                while(not self.isOK(r)):
                    r=random.randrange(0,64)
                self.isOK(r,True)
                
                t=True
                
                self.turn=3-self.turn
                for index_i,i in enumerate(self.field):
                    for index_j,j in enumerate(i):
                        if self.isOK(index_i*8+index_j):
                            t=False
                self.turn=3-self.turn
                
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
            
        self.finish=f
        
        #報酬計算
        
        # 角は常に重視(場合分けなし)
        #-10手目：真ん中の4*4を重視
        #11-50：エッジの部分重視
        #51-64 :総数重視


        for i in self.field[2:6]:
            for j in i[2:6]:
                if j==self.turn:
                    reward+=0.0625
                    
        for i in range(4):
            batch=self.field[0][2:6]
            reward+=batch.count(self.turn)*0.125
            if batch.count(3-self.turn)==0:
                if self.field[0][1]==self.turn:
                    reward+=0.1
                if self.field[0][6]==self.turn:
                    reward+=0.1
                    
            self.field=[list(x) for x in zip(*self.field)][-1::-1]
            
        reward+=(self.black/max(self.white,1))
            
        if self.field[0][0]==1:
            reward+=0.1
        elif self.field[0][0]==2:
            reward-=0.1
        
        if self.field[0][7]==1:
            reward+=0.1
        elif self.field[0][7]==2:
            reward-=0.1
        
        if self.field[7][0]==1:
            reward+=0.1
        elif self.field[7][0]==2:
            reward-=0.1
        
        if self.field[7][7]==1:
            reward+=0.1
        elif self.field[7][7]==2:
            reward-=0.1
            
        # 報酬計算終わり      
                
        if wrong:
            reward=0
            self.finish=True
                
        state=np.array(self.field)
        for index_i,i in enumerate(self.field):
            for index_j,j in enumerate(i):
                if(self.isOK(index_i*8+index_j)):
                    state[index_i][index_j]=3
                
        state=np.reshape(state,(64))

        if not wrong:
            if(self.black>self.white):
                info["result"]="black"
            elif (self.black<self.white):
                info["result"]="white"
            else:
                info["result"]="draw"
                
            if not self.finish:
                info["result"]="playing"
        else:
            info["result"]="wrong"

        return state,reward,self.finish,info

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
        for index_i,i in enumerate(self.field):
            for index_j,j in enumerate(i):
                if(self.isOK(index_i*8+index_j)):
                    state[index_i][index_j]=3
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
    state=a.reset()
    state=state.reshape((8,8))
    print(state)