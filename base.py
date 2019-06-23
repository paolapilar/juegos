
import math
import utils

class Entity( object ) :

    def __init__( self, i, j, di, dj, cellSize, canvasWidth, canvasHeight ) :
        super( Entity, self ).__init__()

        self.i = i
        self.j = j

        self._cellSize = cellSize
        self._canvasWidth = canvasWidth
        self._canvasHeight = canvasHeight
        self._di = di
        self._dj = dj

        self._x, self._y = utils.grid2screen( i, j, cellSize, canvasWidth, canvasHeight )
        self._w = di * cellSize
        self._h = dj * cellSize

        self._xc = self._x + self._cellSize * ( math.floor( ( self._di - 1 ) / 2. ) + 0.5 if self._di % 2 == 0 else 0.0 )
        self._yc = self._y + self._cellSize * ( math.floor( ( self._dj - 1 ) / 2. ) + 0.5 if self._dj % 2 == 0 else 0.0 )

    def x( self ) :
        return self._x

    def y( self ) :
        return self._y

    def xc( self ) :
        return self._xc

    def yc( self ) :
        return self._yc

    def w( self ) :
        return self._w

    def h( self ) :
        return self._h

    def update( self ) :
        self._x, self._y = utils.grid2screen( self.i, self.j, 
                                              self._cellSize, 
                                              self._canvasWidth, 
                                              self._canvasHeight )

        self._xc = self._x + self._cellSize * ( math.floor( ( self._di - 1 ) / 2. ) + 0.5 if self._di % 2 == 0 else 0.0 )
        self._yc = self._y + self._cellSize * ( math.floor( ( self._dj - 1 ) / 2. ) + 0.5 if self._dj % 2 == 0 else 0.0 )

    def hit( self, other ) :
        _dx = abs( self._xc - other.xc() )
        _dy = abs( self._yc - other.yc() )

        if ( _dx < ( self._w / 2. ) + ( other.w() / 2. ) and
             _dy < ( self._h / 2. ) + ( other.h() / 2. ) ) :
            return True
        else :
            return False