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

    def step(self,act):
        ok=self.isOK(act)
        if ok:
            self.isOK(act,True)
            print(self.field)

        f=True
        for i in self.field:
            for j in i:
                if j==0:
                    f=False
        self.finish=f

    def isOK(self,act,shift=False):
        vec=[-1,0,1]
        ok=True

        for i in vec:
            for j in vec:
                if i==0 and j==0:
                    continue
                if(not self.isOK_sub(act,i,j,shift)):
                    ok=False

        return ok

    def isOK_sub(self,act,i,j,shift):
        n_i=act/8
        n_j=act%8
        next=(n_i+i)*8+n_j+j

        if not (0<=n_i+i<8 and 0<=n_j+j<8):
            return False

        if self.field[n_i+i][n_j+j]==self.turn:
            result=self.isOK_sub(next,i,j)
            if result:
                self.field[n_i+i][n_j+j]=3-self.field[n_i+i][n_j+j]
            return result
        elif self.field[n_i+i][n_j+j]==0:
            return False
        else:
            self.field[n_i+i][n_j+j]=3-self.field[n_i+i][n_j+j]
            return True


if __name__=="__main__":
    a=Othello()
    while(a.finish==False):
        a.step(random.randrange(0,81))