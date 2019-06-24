
import pygame
import world

class Text( object ) :

    def __init__( self, x, y, message, size, color ) :
        super( Text, self).__init__()

        self._message = message
        self._textFont = pygame.font.Font( None, size )
        self._textSurface = self._textFont.render( message, True, color )
        self._textRect = self._textSurface.get_rect()
        self._textRect.center = ( x, y )

    def draw( self, canvas ) :
        canvas.blit( self._textSurface, self._textRect )

class Screen( object ) :

    def __init__( self, canvas, backgroundColor ) :
        super( Screen, self ).__init__()

        self._canvas = canvas
        self._backgroundColor = backgroundColor
        self._texts = []

        self._keys = None

    def setKeys( self, keys ) :
        self._keys = keys

    def addText( self, text ) :
        self._texts.append( text )

    def draw( self ) :
        self._canvas.fill( self._backgroundColor )

        for i in range( len( self._texts ) ) :
            self._texts[i].draw( self._canvas )

    def update( self ) :
        pass

class MenuScreen( Screen ) :

    def __init__( self, canvas ) :
        super( MenuScreen, self ).__init__( canvas, ( 255, 255, 0 ) )

        self._textTitle = Text( 100, 100, 'SNAKE', 50, ( 0, 0, 0 ) )
        self._textPlay = Text( 100, 400, 'PLAY', 40, ( 255, 255, 255 ) )

        self.addText( self._textTitle )
        self.addText( self._textPlay )

class GameOverScreen( Screen ) :

    def __init__( self, canvas ) :
        super( GameOverScreen, self ).__init__( canvas, ( 0, 0, 0 ) )

        self._textGameOver = Text( 100, 100, 'GAME OVER :(', 50, ( 255, 0, 255 ) )
        self._textContinue = Text( 100, 400, 'Continue???', 40, ( 255, 255, 255 )  )

        self.addText( self._textGameOver )
        self.addText( self._textContinue )

class GameScreen( Screen ) :

    def __init__( self, canvas, canvasWidth, canvasHeight ) :
        super( GameScreen, self ).__init__( canvas, ( 255, 255, 255 ) )

        self._world = world.World( 40, canvasWidth, canvasHeight )

    def draw( self ) :
        super( GameScreen, self ).draw()

        self._world.draw( self._canvas )

    def update( self ) :
        self._world.setKeys( self._keys )
        self._world.update()

    def lose( self ) :
        return self._world.lose()

    def win( self ) :
        return self._world.win()