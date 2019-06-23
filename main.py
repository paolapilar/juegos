
import pygame
import random
import time

from snake import Snake
from collectables import Apple

class Game :

    def __init__( self ) :
        self._canvas = None
        self._snake = None
        self._gameExit = False
        self._gameOver = False
        self._canvasWidth = 800
        self._canvasHeight = 600
        self._backgroundColor = (255,255,255)

        self._cellSize = 20
        self._nx = int( self._canvasWidth / self._cellSize )
        self._ny = int( self._canvasHeight / self._cellSize )

        self._apples = []

        self._keys = { 'up' : False, 'down' : False, 'right' : False, 'left' : False }

    def init( self ) :
        # initializar pygame
        pygame.init()
        # crear la superficie donde dibujar
        self._canvas = pygame.display.set_mode( ( self._canvasWidth, self._canvasHeight ) )
        # crear la serpiente
        self._snake = Snake( int( self._nx / 2. ), 
                             int( self._ny / 2. ),
                             self._cellSize,
                             self._canvasWidth,
                             self._canvasHeight )

        for _ in range( 10 ) :
            _i = random.randint( 1, self._nx - 1 )
            _j = random.randint( 1, self._ny - 1 )

            self._apples.append( Apple( _i, _j, self._cellSize, self._canvasWidth, self._canvasHeight ) )

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
            self._apples[i].update()
            if self._snake.head().hit( self._apples[i] ) :
                self._snake.grow()
                self._apples[i]._alive = False

        _newApples = []
        for apple in self._apples :
            if apple._alive :
                _newApples.append( apple )

        self._apples = _newApples

        for apple in self._apples :
            apple.draw( self._canvas )

    def _drawGrid( self ) :
        for i in range( self._nx ) :
            xline = ( i + 1 ) * self._cellSize
            pygame.draw.line( self._canvas, 
                              ( 0, 0, 0 ),
                              ( xline, 0 ), 
                              ( xline, self._canvasHeight ),
                              1 )

        for j in range( self._ny ) :
            yline = ( j + 1 ) * self._cellSize
            pygame.draw.line( self._canvas, 
                              ( 0, 0, 0 ),
                              ( 0, yline ), 
                              ( self._canvasWidth, yline ),
                              1 )

    def run( self ) :
        
        while not self._gameExit :
            # dibujar background
            self._canvas.fill( self._backgroundColor )

            self._getEvents()
            self._drawGrid()
            self._updateGame()

            # actualizar el canvas
            pygame.display.update()
            # esperar un ratito
            time.sleep( 0.001 )

if __name__ == '__main__' :
    _game = Game()
    _game.init()
    _game.run()