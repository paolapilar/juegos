
import pygame
import base

from collections import deque

class SnakePart( base.Entity ) :
    
    def __init__( self, i, j, color, cellSize, canvasWidth, canvasHeight ) :
        super( SnakePart, self ).__init__( i, j, 1, 1, cellSize, canvasWidth, canvasHeight )

        self.color = color
        self.lasti = i
        self.lastj = j

    def draw( self, canvas ) :
        _xleft = self._x - 0.5 * self._cellSize 
        _ytop = self._y - 0.5 * self._cellSize

        pygame.draw.rect( canvas, 
                          self.color, 
                          (_xleft, _ytop, self._w, self._h) )	

class Snake( base.Entity ) :

    def __init__( self, i, j, cellSize, canvasWidth, canvasHeight ) :
        super( Snake, self ).__init__( i, j, 1, 1, cellSize, canvasWidth, canvasHeight )

        self._bodyParts = [ SnakePart( i, j, ( 50, 50, 50 ), cellSize, canvasWidth, canvasHeight ) ]
        self._speed = 800.
        self._direction = 'left'
        self._displacement = 0.0
        self._frameTime = 0.001

        self._nx = int( canvasWidth / cellSize )
        self._ny = int( canvasHeight / cellSize )

        self._alive = True

    def alive( self ) :
        return self._alive

    def head( self ) :
        return self._bodyParts[0]

    def tail( self ) :
        return self._bodyParts[-1]

    def setDirection( self, direction ) :
        if len( self._bodyParts ) > 1 :
            # chequear si quieren ir a la direccion contraria
            if ( self._direction == 'left' and direction == 'right' or
                 self._direction == 'right' and direction == 'left' or
                 self._direction == 'up' and direction == 'down' or
                 self._direction == 'down' and direction == 'up' ) :
                # mantener la misma direccion
                self._direction = self._direction
            else :
                # cambiar la direction
                self._direction = direction
        else :
            self._direction = direction

    def grow( self ) :
        _i = self.tail().lasti
        _j = self.tail().lastj

        _newPart = SnakePart( _i, _j, 
                              ( 50, 50, 50 ), 
                              self._cellSize, 
                              self._canvasWidth, 
                              self._canvasHeight )
        self._bodyParts.append( _newPart )

    def update( self ) :
        self._displacement = self._displacement + self._speed * self._frameTime
        if self._displacement > self._cellSize :
            self.head().lasti = self.head().i
            self.head().lastj = self.head().j
            # mover una casilla en la direccion adecuada
            if self._direction == 'up' :
                self.head().j += 1
            elif self._direction == 'down' :
                self.head().j -= 1
            elif self._direction == 'right' :
                self.head().i += 1
            elif self._direction == 'left' :
                self.head().i -= 1

            for k in range( 1, len( self._bodyParts ) ) :
                self._bodyParts[k].lasti = self._bodyParts[k].i
                self._bodyParts[k].lastj = self._bodyParts[k].j

                self._bodyParts[k].i = self._bodyParts[k-1].lasti
                self._bodyParts[k].j = self._bodyParts[k-1].lastj

            # resetear el acumulador
            self._displacement = 0.0

        if self.head()._x > 800. and self._direction == 'right' :
            self.head().i = 0
        
        if self.head()._x < 0. and self._direction == 'left' :
            self.head().i = self._nx

        if self.head()._y > 600. and self._direction == 'down' :
            self.head().j = self._ny
        
        if self.head()._y < 0. and self._direction == 'up' :
            self.head().j = 0
        
        for k in range( len( self._bodyParts ) ) :
            self._bodyParts[k].update()

        for i in range( 1, len( self._bodyParts ) ) :
            if self.head().hit( self._bodyParts[i] ):
                self._alive = False

    def draw( self, canvas ) :
        for k in range( len( self._bodyParts ) ) :
            self._bodyParts[k].draw( canvas )
            
        ## # la misma forma de iterar
        ## for bodyPart in self._bodyParts :
        ## 	 bodyPart.draw( canvas )