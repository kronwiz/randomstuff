from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty


class Blocco ( Widget ):
	# impostata qui come attributo di classe perche' mi serve prima di aver
	# caricato il primo blocco
	WIDTH = 35


class Stage ( Widget ):
	velocita_x = -1
	velocita_y = 0


	def __init__ ( self, **kwargs ):
		super ( Stage, self ).__init__ ( **kwargs )

		self.blocchi = []

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

			if b.x <= Blocco.WIDTH:
				b.x = Window.width



class ScrollerApp ( App ):
	def build ( self ):
		return Stage ()


if __name__ == '__main__':
    ScrollerApp ().run ()

