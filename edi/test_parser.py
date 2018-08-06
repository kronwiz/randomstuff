#!/usr/bin/python3

from lark import Lark
import os.path

def main ():
	fin = open ( "grammar.lark" )
	grammar = fin.read ()
	fin.close ()

	parser = Lark ( grammar, parser = "lalr" )
	#parser = Lark ( grammar, parser = "lalr", lexer = "contextual" )
	#parser = Lark ( grammar )

	count = 1
	testfile = "./test%s.txt" % count
	while os.path.exists ( testfile ):
		print ( "\n\n--- Parsing file: %s ---\n" % testfile )
		fin = open ( testfile )
		try:
			buf = fin.read ()
			print ( buf )

			# Debug lexer
			print ( "Lexer: ", [ x for x in parser.lex ( buf ) ], "\n" )

			tree = parser.parse ( buf )

			print ( tree, "\n\n" )

			print ( tree.pretty () )

		finally:
			fin.close ()

		count += 1
		testfile = "./test%s.txt" % count



if __name__ == '__main__':
	main ()

