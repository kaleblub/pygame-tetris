import pygame
import pickle
from random import randint, randrange, choice
# ----------- Game Initialization -------------------
pygame.init()

displayWidth, displayHeight = 700, 800

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

# ----------- Constants ---------------
menuFont = pygame.font.SysFont(None, 200)
secondaryFont = pygame.font.SysFont(None, 100)
buttonFont = pygame.font.SysFont(None, 75)

FPS = 20
tileSize = 20
backgroundColor = "black"
mainTextColor = "lightgoldenrod1"
boardWidth = 10
boardHeight = 20

# Build A List Of Colored Tiles To Use For The Shapes
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
colorList = [pygame.Surface((tileSize, tileSize)) for i in range(len(colors))]
for i in range(len(colors)):
	colorList[i].fill(colors[i])


shapeRotationsList = [ # The Shapes With Each Of Their Rotations
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

class Button:
	"""Class for a button. Create a button, 
	then blit the surface in the while loop"""
	def __init__(self, text, pos, font, textColor="white", bg=backgroundColor, feedback=""):
		self.x, self.y = pos
		self.font = font
		self.textColor = textColor
		if feedback == "":
			self.feedback = "text"
		else:
			self.feedback = feedback
		self.changeText(text, textColor, bg)

	def changeText(self, text, textColor, bg=backgroundColor):
		"""Change the text when you click"""
		self.text = self.font.render(text, 1, textColor)
		self.size = self.text.get_size()
		self.surface = pygame.Surface(self.size)
		self.surface.fill(bg)
		self.surface.blit(self.text, (0, 0))
		self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

	def show(self):
		gameDisplay.blit(self.surface, (self.x, self.y))

	def wasClicked(self):
		x, y = pygame.mouse.get_pos()
		if self.rect.collidepoint(x, y):
			return True		

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
		self.x = randint(0, displayWidth)
		self.y = -20
		self.fallSpeed = 10
		self.horizontalMoveSpeed = 0

	def drawShape(self, x: int, y: int): # Method for drawing the shape
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

def randomizedShapeDrop(shapeList):
	if shapeList[-1].y > 70:
		shapeList.append(Shape())
	for shape in shapeList:
		if shape.y >= displayHeight:
			shapeList.remove(shape)
		shape.y += shape.fallSpeed/10
		shape.drawShape(shape.x, shape.y)

# ------------- Main Game Function ---------------
def runGame():
	gameRunning = True 
	mainMenuOpen = True
	showingHighscores = False
	gameOver = False
	currentShape, nextShape = Shape(), Shape() # First two shapes initialized
	shapes = []

# ------------ Start Of Game Loop --------------
	while gameRunning:

# ----------- Game Over Menu -------------------
		if gameOver:
			gameOverText1 = menuFont.render("Game", True, mainTextColor)
			gameOverText2 = menuFont.render("Over", True, mainTextColor)
		while gameOver:
			gameDisplay.fill(backgroundColor)
			randomizedShapeDrop(menuShapes)
			gameDisplay.blit(gameOverText1, (displayWidth/4 - 40, displayHeight/4 - 150))
			gameDisplay.blit(gameOverText2, (displayWidth/4, displayHeight/4))
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
		if mainMenuOpen:
			menuShapes = [Shape()]
			menuText = menuFont.render("Tetris", True, mainTextColor)

			playButton = Button("Play", (displayWidth/3, 400), buttonFont, mainTextColor)
			highscoreButton = Button("Highscores", (displayWidth/3, 500), buttonFont, mainTextColor)

		while mainMenuOpen:
			gameDisplay.fill(backgroundColor)

			randomizedShapeDrop(menuShapes)

			# Blit the Title on the main menu
			gameDisplay.blit(menuText, (displayWidth/4 - 30, displayHeight/4))

			# Show the menu buttons
			playButton.show()
			highscoreButton.show()

			pygame.display.update()

			# Main Menu Input Handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainMenuOpen = False
					gameRunning = False
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameRunning = False
						mainMenuOpen = False
					if event.key == pygame.K_c:
						mainMenuOpen = False
				if event.type == pygame.MOUSEBUTTONUP:
					if playButton.wasClicked():
						mainMenuOpen = False
					elif highscoreButton.wasClicked():
						mainMenuOpen = False
						showingHighscores = True

# -------------- HighScores Screen -------------------
		if showingHighscores:
			highscoreText = secondaryFont.render("Highscores", True, mainTextColor)
			try: # load the previous score if it exists
				with open('score.dat', 'rb') as file:
					score = pickle.load(file)
			except FileNotFoundError:
				score = 100
			scoreText = secondaryFont.render(str(score), True, mainTextColor)
			# HOW TO save the score
			with open('score.dat', 'wb') as file:
				pickle.dump(score, file)

		while showingHighscores:
			gameDisplay.fill(backgroundColor)
			randomizedShapeDrop(menuShapes)
			gameDisplay.blit(highscoreText, (displayWidth/4 - 20, displayHeight/4 - 150))
			gameDisplay.blit(scoreText, (displayWidth/4 - 20, displayHeight/4))
			pygame.display.update()

			# HighScores Screen Input Handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					showingHighscores = False
					gameRunning = False
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						showingHighscores = False
						gameRunning = False
					if event.key == pygame.K_c:
						showingHighscores = False

				# if event.type == pygame.MOUSEBUTTONUP:
				# 	if playButton.wasClicked():
				# 		mainMenuOpen = False
				# 	elif highscoreButton.wasClicked():
				# 		mainMenuOpen = False
				# 		showingHighscores = True

# -------------- Gameplay Handling -------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameRunning = False
			if event.type == pygame.MOUSEBUTTONUP:
				pass
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					currentShape.moveLeft()
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					currentShape.moveRight()
				if event.key == pygame.K_UP or event.key == ord('w'):
					currentShape.rotateShape()
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					currentShape.fallBoost()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					currentShape.stopHorizontalMovement()
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					currentShape.stopHorizontalMovement()
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					currentShape.fallSpeedReset()
				if event.key == pygame.K_q:
					pygame.quit()
					exit()
#  ---------------- Game Code -------------------
		# Draw
		gameDisplay.fill(backgroundColor)

		pygame.display.flip() # Updates the whole screen

		if currentShape.y >= displayHeight:
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