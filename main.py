
import pygame
import random
import time

class Apple( object ) :

	def __init__( self, x, y ) :
		super( Apple, self ).__init__()

		self._x = x
		self._y = y
		self._color = ( 255, 0, 0 )
		self._size = 10
		self._alive = True

	def update( self ) :
		pass

	def draw( self, canvas ) :
		pygame.draw.rect( canvas, 
						  self._color, 
						  (self._x, self._y, self._size, self._size) )


class Snake( object ) :

	def __init__( self, x, y ) :
		super( Snake, self ).__init__()

		self._color = ( 50, 50, 50 )
		self._bodySize = 10
		self._bodyParts = [ [x, y] ]
		self._speed = 0.75
		self._direction = 'left'

	def setDirection( self, direction ) :
		self._direction = direction

	def hit( self, apple ) :
		_dx = abs( self._bodyParts[0][0] - apple._x )
		_dy = abs( self._bodyParts[0][1] - apple._y )

		if ( _dx < ( self._bodySize / 2. ) + ( apple._size / 2. ) and
			 _dy < ( self._bodySize / 2. ) + ( apple._size / 2. ) ) :
			return True
		else :
			return False

	def update( self ) :
		if self._direction == 'up' :
			self._bodyParts[0][1] -= self._speed
		elif self._direction == 'down' :
			self._bodyParts[0][1] += self._speed
		elif self._direction == 'right' :
			self._bodyParts[0][0] += self._speed
		elif self._direction == 'left' :
			self._bodyParts[0][0] -= self._speed

		if self._bodyParts[0][0] > 800. and self._direction == 'right' :
			self._bodyParts[0][0] = 0.
		
		if self._bodyParts[0][0] < 0. and self._direction == 'left' :
			self._bodyParts[0][0] = 800.

		if self._bodyParts[0][1] > 600. and self._direction == 'down' :
			self._bodyParts[0][1] = 0.
		
		if self._bodyParts[0][1] < 0. and self._direction == 'up' :
			self._bodyParts[0][1] = 600.
		

	def draw( self, canvas ) :
		for bodyPart in self._bodyParts :
			pygame.draw.rect( canvas, 
							  self._color, 
							  (bodyPart[0], bodyPart[1], self._bodySize, self._bodySize) )

class GameHandler :

	def __init__( self ) :
		self._canvas = None
		self._snake = None
		self._gameExit = False
		self._gameOver = False
		self._canvasWidth = 800
		self._canvasHeight = 600
		self._backgroundColor = (255,255,255)

		self._apples = []

		self._keys = { 'up' : False, 'down' : False, 'right' : False, 'left' : False }

	def init( self ) :
		# initializar pygame
		pygame.init()
		# crear la superficie donde dibujar
		self._canvas = pygame.display.set_mode( ( self._canvasWidth, self._canvasHeight ) )
		# crear la serpiente
		self._snake = Snake( self._canvasWidth / 2., self._canvasHeight / 2. )

		for _ in range( 10 ) :
			_x = random.random() * self._canvasWidth
			_y = random.random() * self._canvasHeight

			self._apples.append( Apple( _x, _y ) )

	def _getEvents( self ) :
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				self._gameExit = True
			elif event.type == pygame.KEYDOWN :
				if event.key == pygame.K_UP :
					self._keys['up'] = True
				elif event.key == pygame.K_DOWN :
					self._keys['down'] = True
				elif event.key == pygame.K_RIGHT :
					self._keys['right'] = True
				elif event.key == pygame.K_LEFT :
					self._keys['left'] = True
			elif event.type == pygame.KEYUP :
				if event.key == pygame.K_UP :
					self._keys['up'] = False
				elif event.key == pygame.K_DOWN :
					self._keys['down'] = False
				elif event.key == pygame.K_RIGHT :
					self._keys['right'] = False
				elif event.key == pygame.K_LEFT :
					self._keys['left'] = False

	def _updateGame( self ) :
		if self._keys['up'] == True :
			self._snake.setDirection( 'up' )
		elif self._keys['down'] == True :
			self._snake.setDirection( 'down' )
		elif self._keys['right'] == True :
			self._snake.setDirection( 'right' )
		elif self._keys['left'] == True :
			self._snake.setDirection( 'left' )

		self._snake.update()
		self._snake.draw( self._canvas )

		for i in range( len( self._apples ) ) :
			if self._snake.hit( self._apples[i] ) :
				# self._snake.grow()
				self._apples[i]._alive = False

		_newApples = []
		for apple in self._apples :
			if apple._alive :
				_newApples.append( apple )
			else :
				print( 'eaten!' )

		self._apples = _newApples

		for apple in self._apples :
			apple.draw( self._canvas )



	def run( self ) :
		
		while not self._gameExit :
			# dibujar background
			self._canvas.fill( self._backgroundColor )

			self._getEvents()
			self._updateGame()

			# actualizar el canvas
			pygame.display.update()
			# esperar un ratito
			time.sleep( 0.001 )

if __name__ == '__main__' :
	_game = GameHandler()
	_game.init()
	_game.run()