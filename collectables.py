
import pygame
import base

class Apple( base.Entity ) :

    def __init__( self, i, j, cellSize, canvasWidth, canvasHeight ) :
        super( Apple, self ).__init__( i, j, 1, 1, cellSize, canvasWidth, canvasHeight )

        self._color = ( 255, 255, 0 )
        self._alive = True

    def draw( self, canvas ) :
        _xleft = self._x - 0.5 * self._cellSize 
        _ytop = self._y - 0.5 * self._cellSize

        pygame.draw.rect( canvas, 
                          self._color, 
                          (_xleft, _ytop, self._w, self._h) )