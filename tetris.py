import pygame
from random import randint, randrange, choice
# ----------- Game Initialization -------------------
pygame.init()

displayWidth, displayHeight = 700, 800

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

# ----------- Constants ---------------
font = pygame.font.SysFont(None, 100)

FPS = 20
tileSize = 20
boardWidth = 10
boardHeight = 20

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
colorList = [pygame.Surface((tileSize, tileSize)) for i in range(len(colors))]
for i in range(len(colors)):
	colorList[i].fill(colors[i])


shapeRotationsList = [
	[ # Line shape
		[(0,0), (1,0), (2,0), (3,0)], 
		[(0,0), (0,1), (0,2), (0,3)]
	],
	[ # J shape
		[(0,0), (1,0), (2,0), (2,1)], 
		[(1,0), (1,1), (1,2), (0,2)], 
		[(0,0), (0,1), (0,2), (1,2)], 
		[(1,0), (0,0), (0,1), (0,2)]
	],
	[ # L shape
		[(0,0), (0,1), (1,0), (2,0)], 
		[(0,0), (0, 1), (0,2), (1,2)], 
		[(0,1), (1,1), (2,1), (2,0)], 
		[(0,0), (1,0), (1,1), (1,2)]
	],
	[ # T shape
		[(0,0), (1,0), (2,0), (1,1)], 
		[(0,0), (0,1), (1,1), (0,2)], 
		[(1,1), (0,2), (1,2), (2,2)], 
		[(2,0), (1,1), (2,1), (2,2)]
	],
	[ # Z shape
		[(0,0), (1,0), (1,1), (2,1)], 
		[(1,0), (0,1), (1,1), (0,2)]
	],
	[ # S shape
		[(1,0), (2,0), (0,1), (1,1)], 
		[(0,0), (0,1), (1,1), (1,2)]
	],
	[ # Square shape
		[(0,0), (1,0), (0,1), (1,1)]
	],
	
]

class Board:
	"""Class for the tetris board"""
	def __init__(self):
		pass

class Shape:
	"""Class for a single shape"""
	def __init__(self):
		self.color = self.randomColor()
		self.shape = self.randomShape()
		self.currentRotation = self.randomRotation()
		self.currentRotationIndex = self.shape.index(self.currentRotation)
		print(self.currentRotation, self.currentRotationIndex)
		self.x = randint(0, displayWidth)
		self.y = 0
		self.fallSpeed = 10
		self.horizontalMoveSpeed = 0

	def __init__(self, )

	def drawShape(self, x: int, y: int):
		w, h = self.color.get_size()
		for pos in self.currentRotation:
			gameDisplay.blit(self.color, (x + pos[0]*w, y + pos[1]*h))

	def randomColor(self): # Selects a random color
		return choice(colorList)

	def randomShape(self): # Selects random shape from list of shape rotations
		return choice(shapeRotationsList)

	def randomRotation(self): # Selects a random rotation from the shape's possible rotations
		return choice(self.shape)

	def fallBoost(self): # Increases self.fallSpeed from 10 to 20
		self.fallSpeed = 20

	def fallSpeedReset(self): # Reduces self.fallSpeed back to 10 from 20
		self.fallSpeed = 10

	def moveLeft(self): # Decreases the horizontalMoveSpeed of the shape to -10 from 0
		self.horizontalMoveSpeed = -10

	def moveRight(self): # Increases the horizontalMoveSpeed of the shape to 10 from 0
		self.horizontalMoveSpeed = 10

	def stopHorizontalMovement(self): # Sets the horizontalMoveSpeed of the shape back to 0
		self.horizontalMoveSpeed = 0

	def rotateShape(self): # Rotates the shape based off of different options in a list of all possible rotations
		if self.currentRotationIndex == len(self.shape) - 1: # If the shape's rotation index is at the end of the list of possible rotations for that shape
			self.currentRotationIndex = 0 # Reset it to the beginning -> [0]
		else:
			self.currentRotationIndex += 1 # Otherwise, just go up an index in the rotation list
		self.currentRotation = self.shape[self.currentRotationIndex] # And set the shape's rotation to the one at that index

# ------------- Main Game Function ---------------
def runGame():
	gameRunning = True
	mainMenuOpen = True
	gameOver = False
	currentShape, nextShape = Shape(), Shape()
	shapes = []

# ------------ Start Of Game Loop --------------
	while gameRunning:

# ----------- Game Over Menu -------------------
		while gameOver:
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

# ---------------- Main Menu --------------------
		while mainMenuOpen:
			gameDisplay.fill('black')
			font = pygame.font.SysFont(None, 200)
			menuText = font.render("Tetris", True, 'red')
			gameDisplay.blit(menuText, (displayWidth/4, displayHeight/3))
			shapes = []
			pygame.display.update()
			for i in range(1, 15):
				shapes.append(Shape())


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainMenuOpen = False
					gameRunning = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameRunning = False
						mainMenuOpen = False
					if event.key == pygame.K_c:
						mainMenuOpen = False


# -------------- Gameplay Handling -------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameRunning = False
			if event.type == pygame.MOUSEBUTTONUP:
				pass
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					print('moving left')
					currentShape.moveLeft()
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					print('moving right')
					currentShape.moveRight()
				if event.key == pygame.K_UP or event.key == ord('w'):
					print('rotate')
					currentShape.rotateShape()
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					print('down')
					currentShape.fallBoost()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					print('left stop')
					currentShape.stopHorizontalMovement()
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					print('right stop')
					currentShape.stopHorizontalMovement()
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					print('down stop')
					currentShape.fallSpeedReset()
				if event.key == ord('q'):
					pygame.quit()
					sys.exit()
					gameRunning = False

#  ---------------- Game Code -------------------
		# Draw
		gameDisplay.fill("black")

		pygame.display.flip() # Updates the whole screen

		if currentShape.y == displayHeight:
			currentShape, nextShape = nextShape, Shape()
		else:
			currentShape.y += currentShape.fallSpeed
			currentShape.x += currentShape.horizontalMoveSpeed
		currentShape.drawShape(currentShape.x, currentShape.y)


		pygame.display.flip() # Updates the whole screen

		# Update
		pygame.display.update()	# Updates only specific sections
		clock.tick(FPS)

	pygame.quit()
	exit()

if __name__ == "__main__":
	runGame()