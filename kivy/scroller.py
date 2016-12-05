from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty, StringProperty


ALTEZZA = [ 1, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 4, 5, 6, 6, 6, 6, 5, 5, 4, 3, 3, 3, 2, 1 ]


class Blocco ( Widget ):
	# impostata qui come attributo di classe perche' mi serve prima di aver
	# caricato il primo blocco
	WIDTH = 35
	HEIGHT = 35


class Stage ( Widget ):
	velocita_x = -1
	velocita_y = 0

	# +1 per tenere conto dell'eventuale resto della divisione (un blocco dentro
	# alla finestra solo in parte).
	MARGINE_DESTRO = ( Window.width / Blocco.WIDTH + 1 ) * Blocco.WIDTH


	def __init__ ( self, **kwargs ):
		super ( Stage, self ).__init__ ( **kwargs )

		self.blocchi = []
		self.altezza_corrente = 0

		# +1 per tenere conto dell'eventuale resto della divisione (un blocco dentro
		# alla finestra solo in parte).
		# +1 per il blocco in piu' completamente fuori dalla finestra che compare man
		# mano che i blocchi scorrono.
		for k in range ( Window.width / Blocco.WIDTH + 2 ):
			blocco = Blocco ()
			self.blocchi.append ( blocco )
			blocco.y = 0
			blocco.x = Blocco.WIDTH * k

			self.add_widget ( blocco )

		Clock.schedule_interval ( self.scorrimento, 0 )


	def scorrimento ( self, dt ):
		for b in self.blocchi:
			b.pos = Vector ( self.velocita_x, self.velocita_y ) + b.pos

			# quando il blocco e' completamente fuori dallo schermo
			if b.x <= -1 * b.WIDTH:
				b.x = self.MARGINE_DESTRO
				b.y = ALTEZZA [ self.altezza_corrente ] * b.HEIGHT
				self.altezza_corrente += 1
				if self.altezza_corrente >= len ( ALTEZZA ): self.altezza_corrente = 0


class Personaggio ( Widget ):
	stage = ObjectProperty ( None )

	caduta_y = 2

	def __init__ ( self, **kwargs ):
		super ( Personaggio, self ).__init__ ( **kwargs )

#		self.frames = [
#			Image ( "personaggio1.png" ),
#			Image ( "personaggio2.png" )
#		]
		self.frames = [ "personaggio1.png", "personaggio2.png" ]

		self.frame_corrente = 0
		self.frame = "personaggio1.png"

		# questo evento controlla il contatto del personaggio con il suolo
		self.caduta_event = Clock.schedule_interval ( self.caduta, 0 )

		self.animazione_event = Clock.schedule_interval ( self.animazione, 1 / 25.0 )

		# lettura della pressione dei tasti
		Window.bind ( on_key_down = self.key_pressed )


	def caduta ( self, dt ):
		tocca = False
		for b in self.stage.blocchi:
			if self.collide_widget ( b ):
				tocca = True
				break

		if not tocca:
			self.y -= self.caduta_y


	def animazione ( self, dt ):
		self.frame_corrente = 1 - self.frame_corrente  # va bene fino a quando sono solo 2
		self.frame = self.frames [ self.frame_corrente ]


	def key_pressed ( self, keyboard, keycode, scancode, codepoint, modifiers, **kwargs ):
		if keycode == 32:  # space
			self.y += 70


#		if keycode == 273:    # up
#			self.y += 1
#
#		elif keycode == 274:  # down
#			self.y -= 1
#
#		elif keycode == 275:  # right
#			self.x += 1
#
#		elif keycode == 276:  # left
#			self.x -= 1


class ScrollerApp ( App ):
	def build ( self ):
		return Stage ()


if __name__ == '__main__':
    ScrollerApp ().run ()

