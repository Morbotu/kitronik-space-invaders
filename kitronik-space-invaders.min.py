from microbit import*
import neopixel
from random import randint
import music
np=neopixel.NeoPixel(pin0,64)
x=4
S=5
r=[[0]*8]*8
K=[[0]*8]*8
T=1
m=8
N=2
X=2
M=100
a=0
Q=-m
G=-N
U=0
g=[[[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0],],[[0,0,1,1,1,0,0,0],[0,1,0,1,0,1,0,0],[0,0,1,1,1,0,0,0],[0,1,0,1,0,1,0,0],],[[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,0],[0,0,0,0,0,0,0,0],[0,3,0,4,0,3,0,0],],[[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,0],[3,3,3,3,3,3,3,0],[4,4,4,4,4,4,4,0],]]
F=[list(i)for i in g[a%len(g)]]+[[0]*8]*4
display.show(S)
while True:
 if T%X==0:
  del r[0]
  r.append([0]*8)
  del K[7]
  K.insert(0,[0]*8)
 if T%M==0:
  if U==0:
   for i in F:
    del i[7]
    i.insert(0,0)
  if U==1:
   del F[7]
   F.insert(0,[0]*8)
  if U==2:
   for i in F:
    del i[0]
    i.append(0)
  if U==3:
   del F[7]
   F.insert(0,[0]*8)
  if len([i for i in F[7]if i>0]):
   break
  U+=1
  if U>3:
   U=0
 if pin13.read_digital()==0 and x<7 and T-G>=N:
  x+=1
  G=T
 if pin12.read_digital()==0 and x>0 and T-G>=N:
  x-=1
  G=T
 if pin15.read_digital()==0 and T-Q>=m:
  r[6][x]=1
  Q=T
 for i in range(len(np)):
  np[i]=(0,0,0)
 for i in range(8):
  for j in range(8):
   if r[i][j]:
    if F[i][j]:
     F[i][j]-=1
     r[i][j]=0
     continue
    np[j+i*8]=(0,10,0)
   if F[i][j]:
    if randint(0,100)>99:
     K[i+1][j]=1
    np[j+i*8]=(0,0,10)
   if K[i][j]:
    if x==j and i==7:
     S-=1
     K[i][j]=0
     pin1.write_digital(1) 
     display.show(S)
     sleep(10)
     pin1.write_digital(0)
     continue
    np[j+i*8]=(10,0,10)
 np[x+7*8]=(10,0,0)
 np.show()
 T+=1
 if S<=0:
  break
 if len([i for i in F if i==[0,0,0,0,0,0,0,0]])==8:
  a+=1
  display.scroll("Wave "+str(a))
  F=[list(i)for i in g[a%len(g)]]+[[0]*8]*4
  T=1
  Q=-m
  G=-N
  U=0
  if a%len(g)==0 and a!=0:
   M-=1
  display.show(S)
music.play(music.DADADADUM,pin=pin2,wait=False)
display.scroll("Game Over  Wave "+str(a))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
