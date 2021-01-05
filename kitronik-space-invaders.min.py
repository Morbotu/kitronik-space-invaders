from microbit import*
import neopixel
from random import randint
import music


def z(np):
    for i in range(len(np)):
        np[i] = (0, 0, 0)


np = neopixel.NeoPixel(pin0, 64)
x = 4
X = 5
o = [[0 for j in range(8)]for i in range(8)]
M = [[0 for j in range(8)]for i in range(8)]
g = 1
j = 8
x = 2
S = 2
d = 100
e = 0
a = -j
L = -x
J = 0
B = [[[1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], ], [
    [1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], ], ]
A = [list(i)for i in B[e % len(B)]]
display.show(X)
while True:
    if g % S == 0:
        del o[0]
        o.append([0 for i in range(8)])
        del M[7]
        M.insert(0, [0 for i in range(8)])
    if g % d == 0:
        if J == 0:
            for i in A:
                del i[7]
                i.insert(0, 0)
        if J == 1:
            del A[7]
            A.insert(0, [0 for i in range(8)])
        if J == 2:
            for i in A:
                del i[0]
                i.append(0)
        if J == 3:
            del A[7]
            A.insert(0, [0 for i in range(8)])
        if len([i for i in A[7]if i > 0]):
            break
        J += 1
        if J > 3:
            J = 0
    if pin13.read_digital() == 0 and x < 7 and g-L >= x:
        x += 1
        L = g
    if pin12.read_digital() == 0 and x > 0 and g-L >= x:
        x -= 1
        L = g
    if pin15.read_digital() == 0 and g-a >= j:
        o[6][x] = 1
        a = g
    z(np)
    for i in range(8):
        for j in range(8):
            if o[i][j]:
                if A[i][j]:
                    A[i][j] -= 1
                    o[i][j] = 0
                    continue
                np[j+i*8] = (0, 10, 0)
            if A[i][j]:
                if randint(0, 100) > 99:
                    M[i+1][j] = 1
                np[j+i*8] = (0, 0, 10)
            if M[i][j]:
                if x == j and i == 7:
                    X -= 1
                    M[i][j] = 0
                    pin1.write_digital(1)
                    display.show(X)
                    sleep(10)
                    pin1.write_digital(0)
                    continue
                np[j+i*8] = (10, 0, 10)
    np[x+7*8] = (10, 0, 0)
    np.show()
    g += 1
    if X <= 0:
        break
    if len([i for i in A if i == [0, 0, 0, 0, 0, 0, 0, 0]]) == 8:
        e += 1
        display.scroll("Wave "+str(e))
        music.play(music.POWER_UP, pin=pin2)
        A = [list(i)for i in B[e % len(B)]]
        g = 1
        a = -j
        L = -x
        J = 0
        display.show(X)
music.play(music.DADADADUM, pin=pin2)
display.scroll("Game Over  Wave "+str(e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
