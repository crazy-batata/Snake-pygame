import pygame
from random import randint 
from math import floor
from engine import *


TILE_SIZE = 32
screen_size = (TILE_SIZE * 20 , TILE_SIZE * 20)
isRunning = True

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode( ( screen_size[0] , screen_size[1] ) )
pygame.display.set_caption("snake |:")
clock = pygame.time.Clock()


font = pygame.font.Font( "fonts/unifont.ttf" , 64 )
font.bold = True

def getInput():
	keys = pygame.key.get_pressed()
	input_ = ""
	
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		if input_manager["input"] != "LEFT": input_ = "RIGHT"
	elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
		if input_manager["input"] != "RIGHT": input_ = "LEFT"

	if keys[pygame.K_UP] or keys[pygame.K_w]:
		if input_manager["input"] != "DOWN": input_ = "UP" 
	elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
		if input_manager["input"] != "UP": input_ = "DOWN"

	if input_:	manageInput(input_)
def manageInput(new_input):
	if snake_movement_props["canMove"]: return
	
	snake_movement_props["canMove"] = True
	snake_movement_props["counter"] = 0
	
	if (new_input == input_manager["input"] and not snake_movement_props["canMove"]) or (new_input in input_manager["input_list"]): return 
	
	input_manager["input_list"].append(new_input)
def move():
	snake_movement_props["canMove"] = False
	snake_movement_props["counter"] = 0
	dx , dy = 0 , 0


	if input_manager["input_list"]:
		input_manager["input"] = input_manager["input_list"][0]
		input_manager["input_list"].pop(0)

	if input_manager["input"] == "RIGHT"  : dx = TILE_SIZE
	elif input_manager["input"] == "LEFT"  : dx = -TILE_SIZE
	elif input_manager["input"] == "UP"   : dy = -TILE_SIZE
	elif input_manager["input"] == "DOWN"  : dy = TILE_SIZE	

	snakeToSnakeCollistion(dx,dy)
	rect.move_ip(dx,dy)
	snakeToFoodCollistion()

	if rect.x >= screen_size[0] and input_manager["input"] == "RIGHT":
		rect.x = 0
	if rect.x < 0 and input_manager["input"] == "LEFT":
		rect.x = screen_size[0] - TILE_SIZE
	if rect.y >= screen_size[1] and input_manager["input"] == "DOWN":
		rect.y = 0
	if rect.y < 0 and input_manager["input"] == "UP":
		rect.y = screen_size[1] - TILE_SIZE
	
	snake_movement_props["body"].append([rect.x,rect.y])
	snake_movement_props["body"] = snake_movement_props["body"][-snake_movement_props["size"]:]

def snakeToFoodCollistion():
	if rectCollistions(food_rect,snake_movement_props["body"]) or rectCollistion(rect,food_rect):
		food_props["respownFood"] = True
		snake_movement_props["size"] += 1
def snakeToSnakeCollistion(dx,dy):
	moved_rect = rect.move(dx,dy)
	if rectCollistions(moved_rect,snake_movement_props["body"]):
		game_props["game_state"] = "restart"


def changeFoodPos():
	food_rect.x = floor(randint(0,screen_size[0]) / TILE_SIZE) * TILE_SIZE 
	food_rect.y = floor(randint(0,screen_size[1]) / TILE_SIZE) * TILE_SIZE
	if rectCollistions(food_rect,snake_movement_props["body"]):
		changeFoodPos()
def resetGame():
	snake_movement_props["size"] = 1
	rect.topleft = (screen_size[0] / 2 ,screen_size[1] / 2)
	
	changeFoodPos()
	move()

input_manager = { "input" : "RIGHT", "input_list": [] }

move_event = pygame.USEREVENT + 2
pygame.time.set_timer(move_event,int(0.2 * 1000))

# snake
snake_movement_props = { "counter": 0 , "delay": 30 , "size": 1 , "body": [] ,"canMove":True }
rect = pygame.Rect( 0 , 0 , TILE_SIZE , TILE_SIZE )

# food
food_props = { "respownFood": True }
food_rect = pygame.Rect( TILE_SIZE * 20 , TILE_SIZE * 20 , TILE_SIZE , TILE_SIZE )

# game
game_props = { "game_state": "playing..." }
game_over_surf =  font.render( "GAME OVER" , False , "white" )
restart_surf =  font.render( "restart" , False , "white" )

cursor_surf =  font.render( ">" , False , "white" )
cursor_props = { "counter":0, "delay": 30, "show":True }

cover_surf = pygame.Surface( screen.get_size() )
cover_surf.fill( "black" )
cover_surf.set_alpha( 150 )


resetGame()
while isRunning:
	game_state = game_props["game_state"]

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
			if game_props["game_state"] == "restart":
				game_props["game_state"] = "playing..."
				resetGame()
		if event.type == move_event and game_state == "playing...":
			if snake_movement_props["canMove"]:
				move()

	if game_state == "playing...":
		cursor_props["counter"] = 0
		cursor_props["show"] = True

		if food_props["respownFood"]:
			changeFoodPos()
			food_props["respownFood"] = False
		getInput()
		snake_movement_props["counter"] += 1
		if snake_movement_props["counter"] >= snake_movement_props["delay"] and not snake_movement_props["canMove"]:
			snake_movement_props["canMove"] = True

	for i in range(len(snake_movement_props["body"])):
		x = snake_movement_props["body"][i][0]
		y = snake_movement_props["body"][i][1]
		color = "white"
		if i == len(snake_movement_props["body"]) - 1:
			color = "yellow"
		pygame.draw.rect(screen,color,pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
	pygame.draw.rect(screen,"red",food_rect)

	if game_state == "restart":
		screen.blit(cover_surf,(0,0))
		screen.blit(game_over_surf,(((screen.get_width() - game_over_surf.get_width()) / 2), 200))
		screen.blit(restart_surf,((screen.get_width() - restart_surf.get_width()  + 40) / 2, 300))
		
		if cursor_props["show"]: cursor_surf.set_colorkey("black")
		else: cursor_surf.set_colorkey("white")
		
		if cursor_props["counter"] >= cursor_props["delay"]:
			cursor_props["counter"] = 0
			cursor_props["show"] = not cursor_props["show"]
		cursor_props["counter"] += 1

		screen.blit(cursor_surf,(((screen.get_width() - restart_surf.get_width()) / 2) - 40, 300))

	

	pygame.display.update()
	screen.fill( "black" )
	clock.tick( 60 )

pygame.quit()