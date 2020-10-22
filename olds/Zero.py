from keras.layers import Dense
from keras.models import Sequential

import numpy as np
import random
import matplotlib.pyplot as plt
import sys

X=[]
y=[]

for i in range(100):
    X.append([random.randrange(0,10),random.randrange(1,10)])
    y.append([X[i][0]/X[i][1]])
    
X=np.array(X)
y=np.array(y)
print(X)
print(y)
# sys.exit()

model=Sequential()
model.add(Dense(units=32,input_shape=(X[0].shape),activation="relu"))
model.add(Dense(units=32,activation="relu"))
model.add(Dense(units=1,activation="relu"))

model.compile(optimizer="Adam",loss="mse",metrics=["acc"])
model.summary()

history=model.fit(x=X,y=y,epochs=1000,verbose=2,validation_split=0.3,batch_size=10)

fig,ax1=plt.subplots()
ax1.plot(history.history['acc'])
ax2=ax1.twinx()
ax2.plot(history.history['loss'],color="y")
plt.show()
. 
for i in range(10):
    r=model.predict(np.array([X[i]]))
    print("{}/{}={}".format(X[i][0],X[i][1],r[0]))

r=model.predict(np.array([[1,0]]))
print("1/0={}".format(r[0]))
