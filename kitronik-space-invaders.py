from microbit import *
import neopixel
from random import randint
import music


def clear_screen(np):
    """
    Clear the screen without showing it yet.
    """
    for i in range(len(np)):
        np[i] = (0, 0, 0)


np = neopixel.NeoPixel(pin0, 64)
x = 4
lives = 5
playerBullets = [[0 for j in range(8)] for i in range(8)]
enemyBullets = [[0 for j in range(8)] for i in range(8)]
rounds = 1
shootCoolDown = 8
moveSpeed = 2
bulletSpeed = 2
enemySpeed = 100
wave = 0
lastBulletsShot = -shootCoolDown
lastMoved = -moveSpeed
enemyDirection = 0
enemyPatterns = [
    [
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 0],
        [2, 2, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 4, 0, 3, 0, 0],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 0],
        [2, 2, 2, 2, 2, 2, 2, 0],
        [3, 3, 3, 3, 3, 3, 3, 0],
        [4, 4, 4, 4, 4, 4, 4, 0],
    ]
]
enemies = [list(i) for i in enemyPatterns[wave % len(enemyPatterns)]]
for i in range(4):
    enemies.append([0, 0, 0, 0, 0, 0, 0, 0])

display.show(lives)
while True:
    # Move playerBullets.
    if rounds % bulletSpeed == 0:
        del playerBullets[0]
        playerBullets.append([0 for i in range(8)])
        del enemyBullets[7]
        enemyBullets.insert(0, [0 for i in range(8)])

    # Move enemies.
    if rounds % enemySpeed == 0:
        if enemyDirection == 0:
            for i in enemies:
                del i[7]
                i.insert(0, 0)
        if enemyDirection == 1:
            del enemies[7]
            enemies.insert(0, [0 for i in range(8)])
        if enemyDirection == 2:
            for i in enemies:
                del i[0]
                i.append(0)
        if enemyDirection == 3:
            del enemies[7]
            enemies.insert(0, [0 for i in range(8)])
        if len([i for i in enemies[7] if i > 0]):
            break
        enemyDirection += 1
        if enemyDirection > 3:
            enemyDirection = 0

    # Move the player.
    if pin13.read_digital() == 0 and x < 7 and rounds - lastMoved >= moveSpeed:
        x += 1
        lastMoved = rounds
    if pin12.read_digital() == 0 and x > 0 and rounds - lastMoved >= moveSpeed:
        x -= 1
        lastMoved = rounds

    # Fire playerBullet.
    if pin15.read_digital() == 0 and rounds - lastBulletsShot >= shootCoolDown:
        playerBullets[6][x] = 1
        lastBulletsShot = rounds

    clear_screen(np)

    for i in range(8):
        for j in range(8):
            # Draw bullets.
            if playerBullets[i][j]:
                # PlayerBullets colliding with enemies.
                if enemies[i][j]:
                    enemies[i][j] -= 1
                    playerBullets[i][j] = 0
                    continue
                np[j+i*8] = (0, 10, 0)

            # Draw enemies.
            if enemies[i][j]:
                # Spawn enemyBullets.
                if randint(0, 100) > 99:
                    enemyBullets[i+1][j] = 1
                np[j+i*8] = (0, 0, 10)

            # Draw enemyBullets.
            if enemyBullets[i][j]:
                # EnemyBullets collide with player.
                if x == j and i == 7:
                    lives -= 1
                    enemyBullets[i][j] = 0
                    pin1.write_digital(1)
                    display.show(lives)
                    sleep(10)
                    pin1.write_digital(0)
                    continue
                np[j+i*8] = (10, 0, 10)

    # Draw the player.
    np[x+7*8] = (10, 0, 0)
    np.show()
    rounds += 1
    if lives <= 0:
        break
    if len([i for i in enemies if i == [0, 0, 0, 0, 0, 0, 0, 0]]) == 8:
        wave += 1
        display.scroll("Wave " + str(wave))
        enemies = [list(i) for i in enemyPatterns[wave % len(enemyPatterns)]]
        for i in range(4):
            enemies.append([0, 0, 0, 0, 0, 0, 0, 0])
        rounds = 1
        lastBulletsShot = -shootCoolDown
        lastMoved = -moveSpeed
        enemyDirection = 0
        if wave % len(enemyPatterns) == 0 and wave != 0:
            enemySpeed -= 1
        display.show(lives)

music.play(music.DADADADUM, pin=pin2, wait=False)
display.scroll("Game Over  Wave " + str(wave))
