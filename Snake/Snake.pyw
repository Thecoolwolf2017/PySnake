import pygame, os, Special
import Core as c
from sys import exit
from Core import 	ON, OFF, WIDTH, HEIGHT, \
					Text, Button, display, clock, \
					font1, font2, font3,\
					Checkbox, Option
from Player import Snake
from Food import Food

# ---------------------------------------------------------------------------

tickrate_option = 2
chance_option = 2
duration_option = 2
drop_option = False
border_option = False

def game(mode):
	if mode == 3:	# options for custom gameplay settings
		global tickrate_option, chance_option, duration_option, drop_option, border_option	

		if tickrate_option == 1:
			Special.changetickrate(2)
		elif tickrate_option == 3:
			Special.changetickrate(7)
		if chance_option == 1:
			Special.changechance(2)
		elif chance_option == 3:
			Special.changechance(25)
		if duration_option == 1:
			Special.changelast(25)
		elif duration_option == 3:
			Special.changelast(55)

	player = Snake(c.START_U)
	player.snake[-1][2] = player.get() or 'u'
	food = Food(player)
	move_accumulator = 0.0
	running = True

	while running:
		delta = clock.tick(60)
		move_accumulator += delta
		step_ms = 1000.0 / max(Special.TICKRATE, 1)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and player.get() != 'r':
					player.goleft()
					break	# without break turning on the spot is possible
				elif event.key == pygame.K_RIGHT and player.get() != 'l':
					player.goright()
					break
				elif event.key == pygame.K_UP and player.get() != 'd':
					player.goup()
					break
				elif event.key == pygame.K_DOWN and player.get() != 'u':
					player.godown()
					break	
				elif event.key == pygame.K_SPACE:
					break	

		advanced = False
		while move_accumulator >= step_ms:
			move_accumulator -= step_ms
			player.update()
			if border_option:	# teleport implementation needs to be between update and draw
				if player.getx() <= 0 or player.getx() >= WIDTH or player.gety() <= 0 or player.gety() >= HEIGHT:
					if player.getx() <= 0:
						player.setx(WIDTH-20)
					elif player.getx() >= WIDTH:
						player.setx(20)
					elif player.gety() <= 0:
						player.sety(HEIGHT-20)
					elif player.gety() >= HEIGHT:
						player.sety(20)
			if not player.running(border_option):
				running = False
				break
			food.update()
			if mode == 2 or (mode == 3 and drop_option):
				if Special.run(player, advance=True, render=False) == False:
					running = False
					break
			advanced = True
		if not running:
			break

		display.fill(ON)
		pygame.draw.rect(display,OFF,[10,10,WIDTH-20,HEIGHT-20])

		player.draw()
		food.draw()
		if mode == 2 or (mode == 3 and drop_option):
			Special.run(player, advance=False, render=True)	# draw existing power-ups and extra food

		pygame.display.update()

def splash(): # splash screen
	running = True
	while running:

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					running=False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running=False
					pygame.quit()
					exit()
			
		display.fill(ON)
	
		pygame.draw.rect(display,OFF,[10,10,WIDTH-20,HEIGHT-20])				

		logo = pygame.image.load(c.asset_path('GUI', 'logo.png'))
		display.blit(logo,(70,130))

		Desciption = Text("Press RETURN to start", 320, 350, font3)
		Desciption.draw(display, ON)

		Credit = Text("Made for an university project. Seweryn Marcinowski 2022", 197, 460, font1)
		Credit.draw(display, ON)

		pygame.display.update()
		clock.tick(60)

def menu():	# main menu
	running = True
	while running:

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					select()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					c.SOUND_CLICK.play()
					click = True
			
		display.fill(ON)
		pygame.draw.rect(display,OFF,[10,10,WIDTH-20,HEIGHT-20])

		logo = pygame.image.load(c.asset_path('GUI', 'logo.png'))
		display.blit(logo,(70,60))

		mx, my = pygame.mouse.get_pos()

		play = Button("Start game", 320, 260)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			if click: select()
		else:play.draw(display)

		play = Button("Custom", 320, 330)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			if click: custom()
		else: play.draw(display)

		play = Button("Exit", 320, 400)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			if click:
				running=False
				pygame.quit()
				exit()
		else: play.draw(display)

		Credit = Text("Made for an university project. Seweryn Marcinowski 2022", 197, 460, font1)
		Credit.draw(display, ON)

		pygame.display.update()
		clock.tick(60)

def select():	# gamemode choice
	running = True
	while running:
		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					c.SOUND_CLICK.play()
					click = True
			
		display.fill(ON)
		pygame.draw.rect(display,OFF,[10,10,WIDTH-20,HEIGHT-20])

		mx, my = pygame.mouse.get_pos()

		play = Button("Classic", 320, 170)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			Desc = Text("Classic Snake gameplay, no surprises!", 320, 80, font2)
			Desc.draw(display, ON)
			if click: game(1)
		else: play.draw(display)

		play = Button("Pick-ups", 320, 240)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			Desc = Text("This fun mode adds power-ups and debuffs", 320, 80, font2)
			Desc.draw(display, ON)
			if click: game(2)
		else: play.draw(display)

		play = Button("Back", 320, 310)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			Desc = Text("Main menu", 320, 80, font2)
			Desc.draw(display, ON)
			if click: running=False
		else: play.draw(display)

		Credit = Text("Made for an university project. Seweryn Marcinowski 2022", 197, 460, font1)
		Credit.draw(display, ON)

		pygame.display.update()
		clock.tick(60)

# --------------------------------------------------------------------------------------------

# def setting(Name, Descripiton, mx, my, click, option):	Might try this later
# 	global option
# 	Desc = Text(Descripiton, 320, 255, font2)
# 	Title = Option(Name,90,40)
# 	Title.draw(display)

# 	option1 = Option("Low",243,40)
# 	option2 = Option("Default",396,40)
# 	option3 = Option("High",550,40)

# 	if Title.collidepoint(mx,my):
# 		Desc.draw(display, ON)

# 	match option:
# 		case 1:
# 			option1.draw(display, "checked")
# 			option2.draw(display)
# 			option3.draw(display)
# 		case 2:
# 			option1.draw(display)
# 			option2.draw(display, "checked")
# 			option3.draw(display)
# 		case 3:
# 			option1.draw(display)
# 			option2.draw(display)
# 			option3.draw(display, "checked")
			
# 	if option1.collidepoint(mx,my):
# 		Desc.draw(display, ON)
# 		if click:
# 			option = 1
# 	if option2.collidepoint(mx,my):
# 		Desc.draw(display, ON)
# 		if click:
# 			option = 2
# 	if option3.collidepoint(mx,my):
# 		Desc.draw(display, ON)
# 		if click:
# 			option = 3

# -------------------------------custom menu and game init-------------------------------------

def custom():	# This is really dirty and i prolly will revise this in the future
	running = True

	global tickrate_option, chance_option, duration_option, drop_option, border_option

	while running:
		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					c.SOUND_CLICK.play()
					click = True
			
		display.fill(ON)
		pygame.draw.rect(display,OFF,[10,10,WIDTH-20,HEIGHT-20])

		mx, my = pygame.mouse.get_pos()

		# -------------- checkboxes -----------------

		pickups = Checkbox(40,90)
		Desc = Text("Turn on special pickups", 320, 255, font2)
		if pickups.collidepoint(mx,my):
			Desc.draw(display, ON)
			if click:
				if drop_option: 
					drop_option = False
				else:
					drop_option = True
		if drop_option:
			pickups.draw(display, True)
		else:
			pickups.draw(display)

		Desc = Text("Power-ups", 120, 90, font2)
		Desc.draw(display,ON)

		border = Checkbox(346,90)
		Desc = Text("Turn off out of bounds game over", 320, 255, font2)
		if border.collidepoint(mx,my):
			Desc.draw(display, ON)
			if click:
				if border_option: 
					border_option = False
				else:
					border_option = True
		if border_option:
			border.draw(display, True)
		else:
			border.draw(display)

		Desc = Text("Teleport", 420, 90, font2)
		Desc.draw(display,ON)

		# -------------- option 1 -----------------

		Desc = Text("Change the base speed of the snake", 320, 255, font2)
		tickrate = Option("Speed",90,40)
		tickrate.draw(display)

		tickrate1 = Option("Low",243,40)
		tickrate2 = Option("Default",396,40)
		tickrate3 = Option("High",550,40)

		if tickrate.collidepoint(mx,my):
			Desc.draw(display, ON)

		if tickrate_option == 1:
			tickrate1.draw(display, "checked")
			tickrate2.draw(display)
			tickrate3.draw(display)
		elif tickrate_option == 2:
			tickrate1.draw(display)
			tickrate2.draw(display, "checked")
			tickrate3.draw(display)
		else:
			tickrate1.draw(display)
			tickrate2.draw(display)
			tickrate3.draw(display, "checked")
			
		if tickrate1.collidepoint(mx,my):
			Desc.draw(display, ON)
			if click:
				tickrate_option = 1
		if tickrate2.collidepoint(mx,my):
			Desc.draw(display, ON)
			if click:
				tickrate_option = 2
		if tickrate3.collidepoint(mx,my):
			Desc.draw(display, ON)
			if click:
				tickrate_option = 3

		# -------------- pick-ups opitons -----------------

		if drop_option:
			Desc = Text("Change how often do pick-ups spawn", 320, 255, font2)
			chance = Option("Chance",90,140)
			chance.draw(display)

			chance1 = Option("Low",243,140)
			chance2 = Option("Default",396,140)
			chance3 = Option("High",550,140)

			if chance.collidepoint(mx,my):
				Desc.draw(display, ON)

			if chance_option == 1:
				chance1.draw(display, "checked")
				chance2.draw(display)
				chance3.draw(display)
			elif chance_option == 2:
				chance1.draw(display)
				chance2.draw(display, "checked")
				chance3.draw(display)
			else:
				chance1.draw(display)
				chance2.draw(display)
				chance3.draw(display, "checked")
				
			if chance1.collidepoint(mx,my):
				Desc.draw(display, ON)
				if click:
					chance_option = 1
			if chance2.collidepoint(mx,my):
				Desc.draw(display, ON)
				if click:
					chance_option = 2
			if chance3.collidepoint(mx,my):
				Desc.draw(display, ON)
				if click:
					chance_option = 3

			Desc = Text("Change how fast do pick-ups disappear", 320, 255, font2)
			duration = Option("Duration",90,190)
			duration.draw(display)

			duration1 = Option("Low",243,190)
			duration2 = Option("Default",396,190)
			duration3 = Option("High",550,190)

			if duration.collidepoint(mx,my):
				Desc.draw(display, ON)

			if duration_option == 1:
				duration1.draw(display, "checked")
				duration2.draw(display)
				duration3.draw(display)
			elif duration_option == 2:
				duration1.draw(display)
				duration2.draw(display, "checked")
				duration3.draw(display)
			else:
				duration1.draw(display)
				duration2.draw(display)
				duration3.draw(display, "checked")
				
			if duration1.collidepoint(mx,my):
				Desc.draw(display, ON)
				if click:
					duration_option = 1
			if duration2.collidepoint(mx,my):
				Desc.draw(display, ON)
				if click:
					duration_option = 2
			if duration3.collidepoint(mx,my):
				Desc.draw(display, ON)
				if click:
					duration_option = 3

		# -------------- footer -----------------

		play = Button("Start", 320, 330)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			Desc = Text("This fun mode adds power-ups and debuffs", 320, 80, font2)
			if click: game(3)
		else: play.draw(display)

		play = Button("Back", 320, 400)
		if play.collidepoint(mx,my):
			play.draw(display, 'hovered')
			if click: running=False
		else: play.draw(display)

		Credit = Text("Made for an university project. Seweryn Marcinowski 2022", 197, 460, font1)
		Credit.draw(display, ON)

		pygame.display.update()
		clock.tick(60)

# -----------------------------------------------------------------------------------------------------

splash()
menu()
pygame.quit()
exit()
