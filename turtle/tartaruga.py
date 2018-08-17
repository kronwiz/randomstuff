#!/usr/bin/python3

from turtle import *

mode ( "logo" )
colormode ( 255 )

goto ( 0, 0 )
pendown ()
colore = 0

for quadrato in range ( 10 ):
	pencolor ( colore * 2, colore * 10, colore * 10 )

	for lato in range ( 4 ):
		forward ( 100 )
		right ( 90 )

	right ( 36 )
	colore = colore + 2

done ()










def quadrato ():
	goto ( 0, 0 )
	pendown ()
	for t in range ( 4 ):
		forward ( 100 )
		right ( 90 )

	done ()


def triangolo ():
	goto ( 0, 0 )
	pendown ()
	setheading ( 0 )
	forward ( 100 )
	setheading ( 90 )
	forward ( 100 )
	setheading ( 225 )
	forward ( 141 )

	done ()

