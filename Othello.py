import random

class Othello:


    """
    0:None
    1:Black
    2:White
    """
    def __init__(self):
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

    def step(self,act):
        ok=self.isOK(act)
        if ok:
            self.isOK(act,True)
            for i in self.field:
                print(i)
            self.turn=3-self.turn
        else:
            print("You can't put on {}".format(act))

        f=True
        self.Pass=True
        for i in self.field:
            for j in i:
                if j==0:
                    f=False
                if f and isOK(i*8+j):
                    f=False
                    self.Pass=False
                self.turn=3-self.turn
                if f and isOK(i*8+j):
                    f=False
                self.turn=3-self.turn

                
                    
        self.finish=f
        
        return

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
        print()