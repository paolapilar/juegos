
import math

def grid2screen( i, j, cellSize, canvasWidth, canvasHeight ) :
    x = ( i + 0.5 ) * cellSize
    y = canvasHeight - ( j + 0.5 ) * cellSize
    return x, y

def screen2grid( x, y, cellSize, canvasWidth, canvasHeight ) :
    i = math.floor( x / cellSize - 0.5 )
    j = math.floor( ( canvasHeight - y ) / cellSize - 0.5 )
    return i, j