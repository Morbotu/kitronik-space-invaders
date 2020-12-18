from microbit import *
import neopixel
import music

class Game:
	"""
	This is the game class.
	"""
	def __init__(self):
		self.np = neopixel.NeoPixel(pin0, 64)
		self.brightness = 1 # A number from 0 to 100

	def game_start(self):
		self.player = Player(self.np)
		self.bullets = []
		self.enemies = []
		self.enemieShape = [
			[1, 0, 1, 0, 1, 0, 1],
			[0, 1, 0, 1, 0, 1, 0]
		]
		for i in range(len(self.enemieShape)):
			for j in range(len(self.enemieShape[0])):
				if self.enemieShape[i][j] > 0:
					self.enemies.append(Enemy(j, i, self.enemieShape[i][j], self.np))
		self.rounds = 0
		self.lastRound = -3
		self.game_loop()

	def game_loop(self):
		while True:
			# Music sounds.
			beep = False
			boom = False

			# Update sprites.
			if pin15.read_digital() == 0 and self.rounds - self.lastRound >= 3:
				beep = True
				self.bullets.append(Sprite(self.player.x, self.player.y, (0, 5, 0), self.np))
				self.lastRound = self.rounds
			for i in range(len(self.bullets))[::-1]:
				# Check for collision and destroy enemy.
				collide = False
				for j in range(len(self.enemies))[::-1]:
					if self.enemies[j].x == self.bullets[i].x and self.enemies[j].y == self.bullets[i].y:
						self.enemies[j].lives -= 1
						if self.enemies[j].lives == 0:
							del self.enemies[j]
						del self.bullets[i]
						collide = True
						boom = True
						break
				if collide:
					continue
				if self.bullets[i].y == 0:
					del self.bullets[i]
					continue
				self.bullets[i].y -= 1

			# Move enemies according to a set pattern.
			if self.rounds % 40 == 0 and self.rounds != 0:
				for i in self.enemies:
					i.y += 1
			elif self.rounds % 30 == 0 and self.rounds != 0:
				for i in self.enemies:
					i.x -= 1
			elif self.rounds % 20 == 0 and self.rounds != 0:
				for i in self.enemies:
					i.y += 1
			elif self.rounds % 10 == 0 and self.rounds != 0:
				for i in self.enemies:
					i.x += 1
			
			self.player.move()

			# Clear screen but only in memory so there is no flicker.
			for i in range(len(self.np)):
				self.np[i] = (0, 0, 0)

			# Draw all sprites.
			for bullet in self.bullets:
				bullet.draw()
			for enemy in self.enemies:
				enemy.draw()
			self.player.draw()
			self.np.show()
			self.rounds += 1

			# If beep is True use the beep as delay instead of sleep.
			if boom:
				music.pitch(100, duration=100, pin=pin2)
			elif beep:
				music.pitch(500, duration=100, pin=pin2)
			else:
				sleep(100)

class Sprite:
	"""
	This is the class that is used in all sprites.
	Since the function draw is the same everywhere
	it only has to be defined once.
	"""
	def __init__(self, x, y, color, np):
		self.x = x
		self.y = y
		self.color = color
		self.np = np
	
	def draw(self):
		self.np[self.x+self.y*8] = (self.color)

class Player(Sprite):
	"""
	The Player class is an extension on the Sprite class.
	If the left button on the :GAME_ZIP64 is pressed the Player will 
	move left and the other way around.
	"""
	def __init__(self, np):
		super(Player, self).__init__(4, 7, (5, 0, 0), np)

	def move(self):
		if pin13.read_digital() == 0 and self.x < 7:
			self.x += 1
		if pin12.read_digital() == 0 and self.x > 0:
			self.x -= 1

class Enemy(Sprite):
	"""
	TODO
	"""
	def __init__(self, x, y, lives, np):
		super(Enemy, self).__init__(x, y, (0, 0, 5), np)
		self.lives = lives

game = Game()
game.game_start()