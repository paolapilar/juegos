
import math
import random
import pygame

from base import Entity
from snake import Snake
from collectables import Apple

class Obstacle( Entity ) :

    def __init__( self, i, j, di, dj, cellSize, canvasWidth, canvasHeight ) :
        super( Obstacle, self ).__init__( i, j, di, dj, cellSize, canvasWidth, canvasHeight )

        self._color = ( 255, 0, 0 )

    def draw( self, canvas ) :
        _xleft = self._x - 0.5 * self._cellSize 
        _ytop = self._y - 0.5 * self._cellSize

        pygame.draw.rect( canvas, 
                          self._color, 
                          (_xleft, _ytop, self._w, self._h) )

class World( object ) :

    def __init__( self, cellSize, canvasWidth, canvasHeight, level = 1 ) :
        super( World, self ).__init__()

        self._cellSize = cellSize
        self._canvasWidth = canvasWidth
        self._canvasHeight = canvasHeight
        
        self._level = level

        self._nx = int( self._canvasWidth / self._cellSize )
        self._ny = int( self._canvasHeight / self._cellSize )

        self._maxLives = 4
        self._numLives = 4

        self._snake = Snake( int( self._nx / 2. ), 
                             int( self._ny / 2. ),
                             self._cellSize,
                             self._canvasWidth,
                             self._canvasHeight )

        self._gameWin = False
        self._gameOver = False
        self._keys = None

        self._points = 0

        self._font = pygame.font.Font( None, 40 )

        self._obstacles = []
        self._occupied = []
        self._apples = []

        self._createObstacles()
        self._createWalls()

        for obstacle in self._obstacles :
            self._occupied.append( ( obstacle.i, obstacle.j ) )

        self._createApples( 1 )

        if self._level == 1 :
            self._snake._speed = 800.
        elif self._level == 2 :
            self._snake._speed = 2100.
        elif self._level == 3 :
            self._snake._speed = 2100.

    def _createObstacles( self ) :
        if self._level == 1 :
            return
        elif self._level == 2 :
            while len( self._obstacles ) < 5 :
                _i = random.randint(0, self._nx)
                _j = random.randint(0, self._ny)
                if _i == int( self._nx / 2 ) and _j == int( self._ny / 2 ) :
                    continue
                self._obstacles.append( Obstacle( _i, _j, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )

        elif self._level == 3 :
            while len( self._obstacles ) < 10 :
                _i = random.randint(0, self._nx)
                _j = random.randint(0, self._ny)
                if _i == int( self._nx / 2 ) and _j == int( self._ny / 2 ) :
                    continue
                self._obstacles.append( Obstacle( _i, _j, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )

    def _createWalls( self ) :
        if self._level == 1 :
            return
        elif self._level == 2 :
            for i in range( self._nx ) :
                self._obstacles.append( Obstacle( i, 0, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
                self._obstacles.append( Obstacle( i, self._ny - 1, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
            
            for j in range( self._ny ) :
                self._obstacles.append( Obstacle( 0, j, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
                self._obstacles.append( Obstacle( self._nx - 1, j, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
        elif self._level == 3 :
            for i in range( self._nx ) :
                if i == int( self._nx / 2 ) :
                    continue

                self._obstacles.append( Obstacle( i, 0, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
                self._obstacles.append( Obstacle( i, self._ny - 1, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
            
            for j in range( self._ny ) :
                if j == int( self._ny / 2 ) :
                    continue

                self._obstacles.append( Obstacle( 0, j, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )
                self._obstacles.append( Obstacle( self._nx - 1, j, 1, 1, self._cellSize, self._canvasWidth, self._canvasHeight ) )

    def _createApples( self, maxApples = 20 ) :

        while True :
            _i = random.randint( 2, self._nx - 2 )
            _j = random.randint( 2, self._ny - 2 )
            _canCreate = True

            for _occupiedPosition in self._occupied :
                _ioccupied = _occupiedPosition[0]
                _joccupied = _occupiedPosition[1]

                if _i == _ioccupied and _j == _joccupied :
                    _canCreate = False
                    break

            if _canCreate :
                self._apples.append( Apple( _i, _j, self._cellSize, self._canvasWidth, self._canvasHeight ) )

            if len( self._apples ) >= maxApples :
                break

    def setKeys( self, keys ) :
        self._keys = keys

    def restart( self ) :
        self._points = 0
        self._snake = Snake( int( self._nx / 2. ), 
                             int( self._ny / 2. ),
                             self._cellSize,
                             self._canvasWidth,
                             self._canvasHeight )

        if self._level == 1 :
            self._snake._speed = 800.
        elif self._level == 2 :
            self._snake._speed = 2100.
        elif self._level == 3 :
            self._snake._speed = 2100.

        self._apples = []
        self._obstacles = []
        self._occupied = []

        self._createObstacles()
        self._createWalls()

        for obstacle in self._obstacles :
            self._occupied.append( ( obstacle.i, obstacle.j ) )

        self._createApples( 1 )

    def _drawGrid( self, canvas ) :
        for i in range( self._nx ) :
            xline = ( i + 1 ) * self._cellSize
            pygame.draw.line( canvas, 
                              ( 0, 0, 0 ),
                              ( xline, 0 ), 
                              ( xline, self._canvasHeight ),
                              1 )

        for j in range( self._ny ) :
            yline = ( j + 1 ) * self._cellSize
            pygame.draw.line( canvas, 
                              ( 0, 0, 0 ),
                              ( 0, yline ), 
                              ( self._canvasWidth, yline ),
                              1 )

    def _drawScore( self, canvas ) :
        _textSurface = self._font.render( 'Puntaje: %d - Vidas: %d' % ( self._points, self._numLives ),
                                          True,
                                          ( 0, 0, 255 ) )

        _textSurface.get_rect().center = ( 30, 30 )

        canvas.blit( _textSurface, _textSurface.get_rect() )

    def draw( self, canvas ) :
        self._drawGrid( canvas )
        self._snake.draw( canvas )

        for obstacle in self._obstacles :
            obstacle.draw( canvas )

        for apple in self._apples :
            apple.draw( canvas )

        self._drawScore( canvas )
    
    def update( self ) :
        if self._keys :
            if self._keys['up'] == True :
                self._snake.setDirection( 'up' )
            elif self._keys['down'] == True :
                self._snake.setDirection( 'down' )
            elif self._keys['right'] == True :
                self._snake.setDirection( 'right' )
            elif self._keys['left'] == True :
                self._snake.setDirection( 'left' )

        self._snake.update()

        for obstacle in self._obstacles :
            obstacle.update()
            if self._snake.head().hit( obstacle ) :
                self._snake._alive = False

        if not self._snake.alive() :
            self._numLives = self._numLives - 1
            if self._numLives >= 1 :
                self.restart()
            else :
                self._gameOver = True
                return

        for i in range( len( self._apples ) ) :
            self._apples[i].update()
            if self._snake.head().hit( self._apples[i] ) :
                self._apples[i]._alive = False
                self._snake.grow()
                self._points = self._points + 1
                self._createApples( 1 )
                if self._level == 1 and self._points >= 5 :
                    self._level = 2
                    self._numLives = 4
                    self._points = 0
                    self.restart()
                elif self._level == 2 and self._points >= 10 :
                    self._level = 3
                    self._numLives = 4
                    self._points = 0
                    self.restart()
                elif self._level == 3 and self._points >= 15 :
                    self._gameWin = True
                    return

        _newApples = []
        for apple in self._apples :
            if apple._alive :
                _newApples.append( apple )

        self._apples = _newApples

    def lose( self ) :
        return self._gameOver

    def win( self ) :
        return self._gameWin