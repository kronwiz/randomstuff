from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty

import time


class Stage ( Widget ):
	pass


class Palla ( Widget ):
	ostacolo = ObjectProperty ( None )

	velocity_x = 0
	velocity_y = -10

	def on_touch_down ( self, touch ):
		if self.collide_point ( touch.x, touch.y ):
			touch.grab ( self )
			return True

		return super ( Palla, self ).on_touch_down ( touch )


	def on_touch_move ( self, touch ):
		if touch.grab_current is self:
			self.center = touch.pos


	def on_touch_up ( self, touch ):
		if touch.grab_current is self:
			touch.ungrab ( self )

			#anim = Animation ( x = self.x, y = 0, t = "out_bounce" )
			#anim.start ( self )
			self.caduta_event = Clock.schedule_interval ( self.caduta_libera, 1.0 / 60.0 )


	def caduta_libera ( self, dt ):
		if ( self.y > 0 ) and ( not self.collide_widget ( self.ostacolo ) ):
			self.pos = Vector ( self.velocity_x, self.velocity_y ) + self.pos

		else:
			self.caduta_event.cancel ()



class Ostacolo ( Widget ):
	pass


class PallinaApp ( App ):
	def build ( self ):
		return Stage ()


if __name__ == '__main__':
    PallinaApp ().run ()
