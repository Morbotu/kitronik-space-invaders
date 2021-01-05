from microbit import*
import neopixel
from random import randint
import music
def L(np):
 for i in range(len(np)):
  np[i]=(0,0,0)
np=neopixel.NeoPixel(pin0,64)
x=4
T=5
q=[[0 for j in range(8)]for i in range(8)]
O=[[0 for j in range(8)]for i in range(8)]
w=1
e=8
F=2
k=2
B=100
h=0
n=-e
I=-F
E=0
u=[[[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0],],[[0,0,1,1,1,0,0,0],[0,1,0,1,0,1,0,0],[0,0,1,1,1,0,0,0],[0,1,0,1,0,1,0,0],],[[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,0],[0,0,0,0,0,0,0,0],[0,3,0,4,0,3,0,0],],[[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,0],[3,3,3,3,3,3,3,0],[4,4,4,4,4,4,4,0],]]
D=[list(i)for i in u[h%len(u)]]
for i in range(4):
 D.append([0,0,0,0,0,0,0,0])
display.show(T)
while True:
 if w%k==0:
  del q[0]
  q.append([0 for i in range(8)])
  del O[7]
  O.insert(0,[0 for i in range(8)])
 if w%B==0:
  if E==0:
   for i in D:
    del i[7]
    i.insert(0,0)
  if E==1:
   del D[7]
   D.insert(0,[0 for i in range(8)])
  if E==2:
   for i in D:
    del i[0]
    i.append(0)
  if E==3:
   del D[7]
   D.insert(0,[0 for i in range(8)])
  if len([i for i in D[7]if i>0]):
   break
  E+=1
  if E>3:
   E=0
 if pin13.read_digital()==0 and x<7 and w-I>=F:
  x+=1
  I=w
 if pin12.read_digital()==0 and x>0 and w-I>=F:
  x-=1
  I=w
 if pin15.read_digital()==0 and w-n>=e:
  q[6][x]=1
  n=w
 L(np)
 for i in range(8):
  for j in range(8):
   if q[i][j]:
    if D[i][j]:
     D[i][j]-=1
     q[i][j]=0
     continue
    np[j+i*8]=(0,10,0)
   if D[i][j]:
    if randint(0,100)>99:
     O[i+1][j]=1
    np[j+i*8]=(0,0,10)
   if O[i][j]:
    if x==j and i==7:
     T-=1
     O[i][j]=0
     pin1.write_digital(1)
     display.show(T)
     sleep(10)
     pin1.write_digital(0)
     continue
    np[j+i*8]=(10,0,10)
 np[x+7*8]=(10,0,0)
 np.show()
 w+=1
 if T<=0:
  break
 if len([i for i in D if i==[0,0,0,0,0,0,0,0]])==8:
  h+=1
  display.scroll("Wave "+str(h))
  D=[list(i)for i in u[h%len(u)]]
  for i in range(4):
   D.append([0,0,0,0,0,0,0,0])
  w=1
  n=-e
  I=-F
  E=0
  if h%len(u)==0 and h!=0:
   B-=1
  display.show(T)
music.play(music.DADADADUM,pin=pin2,wait=False)
display.scroll("Game Over  Wave "+str(h))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
