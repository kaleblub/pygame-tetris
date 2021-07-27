import pygame
from random import randint
# ----------- Game Initialization -------------------
pygame.init()

displayWidth, displayHeight = 700, 800

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Tetris')

# ----------- Constants ---------------
# Game Colors In RGB
# white = (255,255,255)
# black = (0,0,0)
# red = (255,0,0)
# green = (0,155,0)
# blue = (0, 0, 255)
# yellow = (255,255,0)
# orange = (255,165,0)

font = pygame.font.SysFont(None, 100)

tileSize = 20

# redTile = pygame.Surface((tileSize, tileSize))
# redTile.fill("red")
# blueTile = pygame.Surface((tileSize, tileSize))
# blueTile.fill("blue")
# greenTile = pygame.Surface((tileSize, tileSize))
# greenTile.fill("green")
# yellowTile = pygame.Surface((tileSize, tileSize))
# yellowTile.fill("yellow")
# orangeTile = pygame.Surface((tileSize, tileSize))
# orangeTile.fill("orange")
# purpleTile = pygame.Surface((tileSize, tileSize))
# purpleTile.fill("purple")
# WHY CAN'T I PUT 'pygame.Surface' into list comprehension

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
colorList = [pygame.Surface((tileSize, tileSize)) for i in range(len(colors))]
for i in range(len(colors)):
	colorList[i].fill(colors[i])

boardWidth = 10
boardHeight = 20

tileSize = 20

shapes = [
	[(0,0), (1,0), (2,0), (3,0)], # Line shape
	[(0,0), (1,0), (0,1), (1,1)], # Square shape
	[(0,0), (1,0), (2,0), (2,1)], # L shape
	[(0,0), (0,1), (1,0), (2,0)], # Reverse L shape
	[(0,0), (1,0), (2,0), (1,1)], # T shape
]

def drawShape(x, y, tileIndex, surface):
	w, h = surface.get_size()
	for position in shapes[tileIndex]:
		gameDisplay.blit(surface, (x + position[0]*w, y + position[1]*h))

# Class for the shapes
class Shape:
	def __init__(self):
		self.color = self.randomColor(randint(0, len(colorList)))
		self.shape = self.randomShape()
		self.x = 0
		self.y = 0
		self.fallSpeed = 20

	def randomColor(self, num): # Selects a random color
		return colorList[num]

	def randomShape(self): # Selects random shape from list of 'shapes'
		return shapes[randint(0, len(shapes))]

	def fallBoost(self):
		fallSpeed = 40

	def fallSpeedReset(self):
		fallSpeed = 20

	def rotateShape():
		pass
	
	def drawShape(self, x, y):
		w, h = self.color.get_size()
		for pos in shapes[self.shape]:
			gameDisplay.blit(self.color, (x + pos[0]*w, y + pos[1]*h))

# ------------- Main Game Function ---------------
def runGame():
	gameRunning = True
	gameOver = False

# ------------ Start Of Game Loop --------------
	while gameRunning:

# ----------- Game Over Menu -------------------
		while gameOver == True:
			gameDisplay.fill(white)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameRunning = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameRunning = False
						gameOver = False
					if event.key == pygame.K_c:
						runGame()

# -------------- Gameplay Handling -------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameRunning = False
			if event.type == pygame.MOUSEBUTTONUP:
				pass
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					print('left')
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					print('right')
				if event.key == pygame.K_UP or event.key == ord('w'):
					print('jump')
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					print('down')

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					print('left stop')
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					print('right stop')
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					print('down stop')
				if event.key == ord('q'):
					pygame.quit()
					sys.exit()
					gameRunning = False

#  ----------- Game Code -------------------
		# Draw
		gameDisplay.fill("black")

		# RANDOMIZE THE SHAPE & COLOR
		#				  |	   |
		#				  v    v
		randomX, randomY = randint(0, displayWidth), randint(0, displayHeight)

		drawShape(randomX, randomY)
		pygame.display.flip() # Updates the whole screen

		# Update
		pygame.display.update()	# Updates only specific sections


	pygame.quit()
	exit()

if __name__ == "__main__":
	runGame()