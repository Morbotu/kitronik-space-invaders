from microbit import*
import neopixel
from random import randint
import music
np=neopixel.NeoPixel(pin0,64) 
x=4 
f=5 
U=[[0 for j in range(8)]for i in range(8)]
D=[[0 for j in range(8)]for i in range(8)]
b=1 
l=8
u=2
P=2 
B=100 
h=0 
I=-l
i=-u 
R=0 
X=[[[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0],],[[0,0,1,1,1,0,0,0],[0,1,0,1,0,1,0,0],[0,0,1,1,1,0,0,0],[0,1,0,1,0,1,0,0],],[[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,0],[0,0,0,0,0,0,0,0],[0,3,0,4,0,3,0,0],],[[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,0],[3,3,3,3,3,3,3,0],[4,4,4,4,4,4,4,0],]]
o=[list(i)for i in X[h%len(X)]]
for i in range(4):
 o.append([0,0,0,0,0,0,0,0])
display.show(f)
while True:
 if b%P==0:
  del U[0]
  U.append([0 for i in range(8)])
  del D[7]
  D.insert(0,[0 for i in range(8)])
 if b%B==0:
  if R==0:
   for i in o:
    del i[7]
    i.insert(0,0)
  if R==1:
   del o[7]
   o.insert(0,[0 for i in range(8)])
  if R==2:
   for i in o:
    del i[0]
    i.append(0)
  if R==3:
   del o[7]
   o.insert(0,[0 for i in range(8)])
  if len([i for i in o[7]if i>0]):
   break
  R+=1
  if R>3:
   R=0
 if pin13.read_digital()==0 and x<7 and b-i>=u:
  x+=1
  i=b
 if pin12.read_digital()==0 and x>0 and b-i>=u:
  x-=1
  i=b
 if pin15.read_digital()==0 and b-I>=l:
  U[6][x]=1
  I=b
 for i in range(len(np)):
  np[i]=(0,0,0)
 for i in range(8):
  for j in range(8):
   if U[i][j]:
    if o[i][j]:
     o[i][j]-=1
     U[i][j]=0
     continue
    np[j+i*8]=(0,10,0)
   if o[i][j]:
    if randint(0,100)>99:
     D[i+1][j]=1
    np[j+i*8]=(0,0,10)
   if D[i][j]:
    if x==j and i==7:
     f-=1
     D[i][j]=0
     pin1.write_digital(1) 
     display.show(f)
     sleep(10)
     pin1.write_digital(0)
     continue
    np[j+i*8]=(10,0,10)
 np[x+7*8]=(10,0,0)
 np.show()
 b+=1
 if f<=0:
  break
 if len([i for i in o if i==[0,0,0,0,0,0,0,0]])==8:
  h+=1
  display.scroll("Wave "+str(h))
  o=[list(i)for i in X[h%len(X)]]
  for i in range(4):
   o.append([0,0,0,0,0,0,0,0])
  b=1
  I=-l
  i=-u
  R=0
  if h%len(X)==0 and h!=0:
   B-=1
  display.show(f)
music.play(music.DADADADUM,pin=pin2,wait=False)
display.scroll("Game Over  Wave "+str(h))