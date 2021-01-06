from microbit import *
import neopixel
from random import randint
import music


np = neopixel.NeoPixel(pin0, 64)  # Alle rgb leds worden bestuurt met neopixel.
x = 4  # x positie van de speler.
lives = 5  # Levens van de speler.
# Matrix van de playerBullets.
playerBullets = [[0 for j in range(8)] for i in range(8)]
# Matrix van de enemyBullets.
enemyBullets = [[0 for j in range(8)] for i in range(8)]
rounds = 1  # Aantal rondes van die de game loop heeft gemaakt.
# Het aantal rondes dat je moet wachten totdat je een nieuwe kogel kan schieten.
shootCoolDown = 8
# Het aantal rondes dat je moet wachten tot je weer een pixel kan bewegen.
moveSpeed = 2
bulletSpeed = 2  # Het aantal rondes tussen iedere verplaatsing van de kogels.
enemySpeed = 100  # Het aantal rondes tussen iedere beweging van de enemies.
wave = 0  # De wave waar je inzit.
# In welke ronde de laatste kogel is geschoten.
lastBulletsShot = -shootCoolDown
lastMoved = -moveSpeed  # In welke ronde de laatste beweging was.
enemyDirection = 0  # De richting waar de enemies zullen heenbewegen.

# Dit zijn alle levels.
# Het is alleen de bovenste helft omdat dat minder ruimte opneemt.
# De onderste helft zijn alleen maar nullen en
# worden toegevoegt als het level geopend wordt.
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

# Hier wordt het level geladen.
# Het gaat op deze manier om te vermijden er pass by reference is.
enemies = [list(i) for i in enemyPatterns[wave % len(enemyPatterns)]]
# Hier worden de laatste vier rijen toegvoegd.
for i in range(4):
    enemies.append([0, 0, 0, 0, 0, 0, 0, 0])

display.show(lives)

# De game loop.
while True:
    # Beweegt playerBullets.
    if rounds % bulletSpeed == 0:
        del playerBullets[0]
        playerBullets.append([0 for i in range(8)])
        del enemyBullets[7]
        enemyBullets.insert(0, [0 for i in range(8)])

    # Beweegt enemies.
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

        # Kijkt of één van de enemies de overkant heeft gehaald.
        # Dan is het spel over.
        if len([i for i in enemies[7] if i > 0]):
            break

        enemyDirection += 1
        if enemyDirection > 3:
            enemyDirection = 0

    # Beweegt de speler.
    if pin13.read_digital() == 0 and x < 7 and rounds - lastMoved >= moveSpeed:
        x += 1
        lastMoved = rounds
    if pin12.read_digital() == 0 and x > 0 and rounds - lastMoved >= moveSpeed:
        x -= 1
        lastMoved = rounds

    # Vuurt playerBullet.
    if pin15.read_digital() == 0 and rounds - lastBulletsShot >= shootCoolDown:
        playerBullets[6][x] = 1
        lastBulletsShot = rounds

    # Zet de waarde van alle pixels op nul maar laat het nog niet op het scherm zien.
    for i in range(len(np)):
        np[i] = (0, 0, 0)

    for i in range(8):
        for j in range(8):
            # Tekend bullets.
            if playerBullets[i][j]:
                # PlayerBullets botst met enemies.
                if enemies[i][j]:
                    enemies[i][j] -= 1
                    playerBullets[i][j] = 0
                    continue
                np[j+i*8] = (0, 10, 0)

            # Tekend enemies.
            if enemies[i][j]:
                # Maakt nieuwe enemyBullets.
                if randint(0, 100) > 99:
                    enemyBullets[i+1][j] = 1
                np[j+i*8] = (0, 0, 10)

            # Teken enemyBullets.
            if enemyBullets[i][j]:
                # EnemyBullets botst met speler.
                if x == j and i == 7:
                    lives -= 1
                    enemyBullets[i][j] = 0
                    pin1.write_digital(1)  # Laat de microbit trillen.
                    display.show(lives)
                    sleep(10)
                    pin1.write_digital(0)
                    continue
                np[j+i*8] = (10, 0, 10)

    # Tekend de speler.
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

# Het einde van het spel.
music.play(music.DADADADUM, pin=pin2, wait=False)
display.scroll("Game Over  Wave " + str(wave))
