import Food
from random import randint
import Core as c

powerup = None
xtrafood = []
x3counter = 0

DROP_CHANCE = 5				# Drop chance per tick global value
DROP_LAST = 40				# Drop wait in ticks global value
BASE_TICKRATE = 4			# Base speed global value

TICKRATE = BASE_TICKRATE	# allows variable tickrate in game

def changetickrate(value):
	global BASE_TICKRATE, TICKRATE
	BASE_TICKRATE = value
	TICKRATE = BASE_TICKRATE

def changechance(value):
	global DROP_CHANCE
	DROP_CHANCE = value

def changelast(value):
	global DROP_LAST
	DROP_LAST = value

class minus1(Food.Food):	#uppercase
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.life = DROP_LAST	# how long the pickup stays on the map
	
	def update(self):
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			if self.player.points == 1:	# if zero points game over
				if self.player.gameover():
					return 0 			# if retry chosen continue loop (game reset in gameover function)
				else:
					return -1
			else:	
				self.player.point(-1)
				del self.player.snake[0]# delete last snake segment
				return 0
		else:
			self.life -= 1
			return self.life

	def draw(self):
		if self.life < 10 and self.life %2:
			super().draw(c.BLANK)		# blinking 5 times before disapearing
		else:
			super().draw(c.MINUS1)

class plus3(Food.Food):
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.life = DROP_LAST
	
	def update(self):
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			self.player.point(3)		# add 3 points
			return 0
		else:
			self.life -= 1
			return self.life

	def draw(self):
		if self.life < 10 and self.life %2:
			super().draw(c.BLANK)
		else:
			super().draw(c.PLUS3)

class times3(Food.Food):
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.life = DROP_LAST
	
	def update(self):
		global x3counter
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			x3counter += 1
			for each in range(x3counter*3):
				xtrafood.append(Food.Food(self.player))	# multiplies the ammount of food that spawns by 3
			return 0
		else:
			self.life -= 1
			return self.life

	def draw(self):
		if self.life < 10 and self.life %2:
			super().draw(c.BLANK)
		else:
			super().draw(c.TIMES3)

class divide(Food.Food):
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.life = DROP_LAST
	
	def update(self):
		global x3counter
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			for each in range(x3counter*3):		# stops food added by times3() from spawning
				xtrafood.pop()
			x3counter -= 1
			return 0
		else:
			self.life -= 1
			return self.life

	def draw(self):
		if self.life < 10 and self.life %2:
			super().draw(c.BLANK)
		else:
			super().draw(c.DIVIDE)

class faster(Food.Food):
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.life = DROP_LAST
	
	def update(self):
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			global TICKRATE
			TICKRATE += 2						# speeds up the game
			return 0
		else:
			self.life -= 1
			return self.life

	def draw(self):
		if self.life < 10 and self.life %2:
			super().draw(c.BLANK)
		else:
			super().draw(c.SPEED)

class slower(Food.Food):
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.life = DROP_LAST
	
	def update(self):
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			global TICKRATE
			TICKRATE -= 2						# slows down the game
			return 0
		else:
			self.life -= 1
			return self.life

	def draw(self):
		if self.life < 10 and self.life %2:
			super().draw(c.BLANK)
		else:
			super().draw(c.SLOW)

def run(player, advance=True, render=True):
	global powerup
	if advance:
		if not powerup:					# only one powerup can spawn
			if randint(1,100) < DROP_CHANCE:	#	default chance of drop
				drop = randint(1,6)
				new_powerup = None
				if drop == 1:
					new_powerup = faster(player)
				elif drop == 2:
					if TICKRATE > BASE_TICKRATE: # won't spawn if game is running at base speed
						new_powerup = slower(player)
				elif drop == 3:
					new_powerup = times3(player)
				elif drop == 4:
					if x3counter != 0:		# won't spawn untill times3() was picked up at least once
						new_powerup = divide(player)
				elif drop == 5:
					new_powerup = minus1(player)
				else:
					new_powerup = plus3(player)
				if new_powerup:
					c.SOUND_SPAWN.play()
					powerup = new_powerup
		else:
			result = powerup.update()	# updating powerups
			if result == 0:				# when picked up or life runs out
				del powerup
				powerup = None
			elif result == -1:			# ends the game loop if user quit in gameover prompt
				return False
	if render and powerup:
		powerup.draw()
	for each in xtrafood:			# spawning food generated by times3()
		if advance:
			each.update()
		if render:
			each.draw()
	return True



  
