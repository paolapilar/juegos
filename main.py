
import pygame
import random
import time

from snake import Snake
from collectables import Apple

import screen

class Game :

    def __init__( self ) :
        pygame.init()
        self._canvasWidth = 800
        self._canvasHeight = 600
        self._canvas = pygame.display.set_mode( ( self._canvasWidth, self._canvasHeight ) )
        self._gameExit = False
        self._keys = { 'up' : False, 
                       'down' : False, 
                       'right' : False, 
                       'left' : False,
                       'enter' : False,
                       'escape' : False }

        self._screen = screen.MenuScreen( self._canvas )
        self._screenName = 'menu'

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
                elif event.key == pygame.K_RETURN :
                    self._keys['enter'] = True
                elif event.key == pygame.K_ESCAPE :
                    self._keys['escape'] = True
            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    self._keys['up'] = False
                elif event.key == pygame.K_DOWN :
                    self._keys['down'] = False
                elif event.key == pygame.K_RIGHT :
                    self._keys['right'] = False
                elif event.key == pygame.K_LEFT :
                    self._keys['left'] = False
                elif event.key == pygame.K_RETURN :
                    self._keys['enter'] = False
                elif event.key == pygame.K_ESCAPE :
                    self._keys['escape'] = False

    def _updateScreen( self ) :
        self._screen.setKeys( self._keys )
        self._screen.update()
        self._screen.draw()

        if self._screenName == 'menu' and self._keys['enter'] == True :
            self._screen = screen.GameScreen( self._canvas, self._canvasWidth, self._canvasHeight )
            self._screenName = 'game'

        elif self._screenName == 'game' and self._screen.lose() :
            self._screen = screen.GameOverScreen( self._canvas )
            self._screenName = 'gameover'

        elif self._screenName == 'game' and self._screen.win() :
            self._screen = screen.MenuScreen( self._canvas ) 
            self._screenName = 'menu'

        elif self._screenName == 'gameover' and self._keys['enter'] == True :
            self._screen = screen.GameScreen( self._canvas, self._canvasWidth, self._canvasHeight )
            self._screenName = 'game'

        elif self._screenName == 'gameover' and self._keys['escape'] == True :
            self._screen = screen.MenuScreen( self._canvas )
            self._screenName = 'menu'

    def run( self ) :
        
        while not self._gameExit :
            self._getEvents()
            self._updateScreen()

            # actualizar el canvas
            pygame.display.update()
            # esperar un ratito
            time.sleep( 0.001 )

if __name__ == '__main__' :
    _game = Game()
    _game.run()