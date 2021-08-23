import pygame

def rectCollistion(rect,other_rect,tile_size = 16):
	if type(rect) == tuple or type(rect) == list:
		if len(rect) == 2:
			rect = pygame.Rect(rect[0],rect[1],tile_size,tile_size) 
		else:
			rect = pygame.Rect(rect[0],rect[1],rect[2],rect[3])


	if type(other_rect) == tuple or type(other_rect) == list:
		if len(other_rect) == 2:
			other_rect = pygame.Rect(other_rect[0],other_rect[1],tile_size,tile_size) 
		else:
			other_rect = pygame.Rect(other_rect[0],other_rect[1],other_rect[2],other_rect[3])

	return rect.colliderect(other_rect)

def rectCollistions(rect,other_rects,tile_size = 16):
	for other_rect in other_rects:
		if rectCollistion(rect,other_rect,tile_size):
			return True
	return False