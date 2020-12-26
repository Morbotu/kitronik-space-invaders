_A=False
from microbit import *
import neopixel,music,micropython
class Game:
	def __init__(self):self.np=neopixel.NeoPixel(pin0,64);self.brightness=1
	def game_start(self):self.player=Player(self.np);self.bullets=[];self.enemies=[];self.wave=0;self.enemieShape=[[[1,0,1,0,1,0,1],[0,1,0,1,0,1,0]],[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]]];self.spawn_enemies();self.rounds=0;self.lastRound=-3;self.enemySpeed=1;self.gameOver=_A;self.game_loop()
	def spawn_enemies(self):
		for i in range(len(self.enemieShape[self.wave])):
			for j in range(len(self.enemieShape[self.wave][0])):
				if self.enemieShape[self.wave][i][j]>0:self.enemies.append(Enemy(j,i,self.enemieShape[self.wave][i][j],self.np))
	def game_loop(self):
		A=True
		while A:
			beep=_A;boom=_A
			if pin15.read_digital()==0 and self.rounds-self.lastRound>=3:beep=A;self.bullets.append(Sprite(self.player.x,self.player.y,(0,5,0),self.np));self.lastRound=self.rounds
			for i in range(len(self.bullets))[::-1]:
				collide=_A
				for j in range(len(self.enemies))[::-1]:
					if self.enemies[j].x==self.bullets[i].x and self.enemies[j].y==self.bullets[i].y:
						self.enemies[j].lives-=1
						if self.enemies[j].lives==0:del self.enemies[j]
						del self.bullets[i];collide=A;boom=A;break
				if collide:continue
				if self.bullets[i].y==0:del self.bullets[i];continue
				self.bullets[i].y-=1
			if self.rounds%(40*self.enemySpeed)==0 and self.rounds!=0:
				for i in self.enemies:
					i.y+=1
					if i.y>7:self.gameOver=A;break
			elif self.rounds%(30*self.enemySpeed)==0 and self.rounds!=0:
				for i in self.enemies:i.x-=1
			elif self.rounds%(20*self.enemySpeed)==0 and self.rounds!=0:
				for i in self.enemies:
					i.y+=1
					if i.y>7:self.gameOver=A;break
			elif self.rounds%(10*self.enemySpeed)==0 and self.rounds!=0:
				for i in self.enemies:i.x+=1
			if self.gameOver:break
			self.player.move()
			for i in range(len(self.np)):self.np[i]=0,0,0
			for bullet in self.bullets:bullet.draw()
			for enemy in self.enemies:enemy.draw()
			self.player.draw();self.np.show();self.rounds+=1
			if boom:music.pitch(100,duration=100,pin=pin2)
			elif beep:music.pitch(500,duration=100,pin=pin2)
			else:sleep(100)
			if len(self.enemies)==0:self.wave+=1;display.scroll('Wave '+str(self.wave),delay=100,wait=A);self.spawn_enemies()
		display.scroll('Game Over',wait=A)
class Sprite:
	def __init__(self,x,y,color,np):self.x=x;self.y=y;self.color=color;self.np=np
	def draw(self):self.np[self.x+self.y*8]=self.color
class Player(Sprite):
	def __init__(self,np):super(Player,self).__init__(4,7,(5,0,0),np)
	def move(self):
		if pin13.read_digital()==0 and self.x<7:self.x+=1
		if pin12.read_digital()==0 and self.x>0:self.x-=1
class Enemy(Sprite):
	def __init__(self,x,y,lives,np):super(Enemy,self).__init__(x,y,(0,0,5),np);self.lives=lives
game=Game()
game.game_start()