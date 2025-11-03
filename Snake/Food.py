import pygame, os
from Core import WIDTH, HEIGHT, display
import Core as c
from random import randint

class Food(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__()
		self.player = player
		self.xfood, self.yfood = 0, 0
		self.xfcords, self.yfcords = [*range(20,WIDTH-10,20)], [*range(20,HEIGHT-10,20)]	# possible locations on the grid
		self.genfood()		# generating initial location on first call

	def getxfood(self):
		return self.xfood
	def getyfood(self):
		return self.yfood

	def genfood(self):
		self.xfood = self.xfcords[randint(0,len(self.xfcords)-1)]
		self.yfood = self.yfcords[randint(0,len(self.yfcords)-1)]
		for segment in self.player.snake:	# food cant spawn inside the snake
			if self.xfood == segment[0] and self.yfood == segment[1]: 
				self.genfood()

	def update(self):
		if self.player.getx() == self.xfood and self.player.gety() == self.yfood:
			c.SOUND_EAT.play()
			self.player.point()
			self.genfood()

	def draw(self, file = c.NORMAL):
		if self.player.getx() + self.player.getmovex() == self.xfood and self.player.gety() + self.player.getmovey()  == self.yfood:
			self.player.openwide()	# snake mouth animation
		display.blit(file, (self.xfood-5,self.yfood-5))
