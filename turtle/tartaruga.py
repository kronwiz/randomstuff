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


def quadrato_colorato_nomi ():
	goto ( 0, 0 )
	setheading ( 0 )
	pendown ()
	pencolor ( "red" )
	forward ( 100 )
	right ( 90 )
	pencolor ( "orange" )
	forward ( 100 )
	right ( 90 )
	pencolor ( "light green" )
	forward ( 100 )
	right ( 90 )
	pencolor ( "green" )
	forward ( 100 )
	right ( 90 )

	done ()


def quadrato_colorato_numeri ():
	goto ( 0, 0 )
	setheading ( 0 )
	pendown ()
	pencolor ( 255, 0, 0 )
	forward ( 100 )
	right ( 90 )
	pencolor ( 255, 165, 0 )
	forward ( 100 )
	right ( 90 )
	pencolor ( 144, 238, 144 )
	forward ( 100 )
	right ( 90 )
	pencolor ( 0, 255, 0 )
	forward ( 100 )
	right ( 90 )

	done ()


def stella_quadrati ():
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


