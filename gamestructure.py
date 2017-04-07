#############################################################
##Name: Taylor Del Matto
##Course: CS 419
##Final Project: Chess Game
##gamestructure
##Description: The classes and functions in this file allow
##us to create the gamestructure object and other gameplay objects
#############################################################

#class creates position objects which denote the position of a piece on the board
class Position(object):
	x = 0
	y = 0

#function creates, returns a position from input
def makeposition(x,y):
	position = Position()
	position.x = x
	position.y = y
	return position

#this class contains arrays that contain all instances of a piece of its type
class Pieces(object):
	pawns = []
	bishops = []
	rooks = []
	knights = []
	queens = []
	king = []

#function creates, returns pieces object
def returnpieces():
	pp = Pieces()
	return pp

#the player class contains variables depicting the game state for an individual player
class Player1(object):
	castleflag = 0
	pawnpflag = 0
	enpassantvalid = []
	checkflag = 0
	playertype = 0
	hrookmoved = 0
	arookmoved = 0
	kingmoved = 0
	color = "W"#change this back to blank string later
	piecestaken = []
	pieces = Pieces()

#this class is the same as the player1 class.  Since these two classes are redundant, they should be combined.  
class Player2(object):
	castleflag = 0
	pawnpflag = 0
	enpassantvalid = []
	checkflag = 0
	playertype = 0
	hrookmoved = 0
	arookmoved = 0
	kingmoved = 0
	color = "W"#change this back to blank string later
	piecestaken = []
	pieces = Pieces()


#this function creates and initializes the positions of the black pieces
def blackPieces():
	piece = Pieces()
	piece.pawns = [makeposition(0,6),makeposition(1,6),makeposition(2,6),makeposition(3,6),makeposition(4,6), makeposition(5,6),makeposition(6,6),makeposition(7,6)]
	piece.bishops = [makeposition(2,7), makeposition(5,7)]
	piece.rooks = [makeposition(0,7), makeposition(7,7)]
	piece.knights = [makeposition(1,7), makeposition(6,7)]
	piece.queens = [makeposition(4,7)]
	piece.king = [makeposition(3,7)]
	return piece

#this function creates and initializes the positions of the white pieces
def whitePieces():
	piece = Pieces()
	piece.pawns = [makeposition(0,1),makeposition(1,1),makeposition(2,1),makeposition(3,1),makeposition(4,1), makeposition(5,1),makeposition(6,1),makeposition(7,1)]
	piece.bishops = [makeposition(2,0), makeposition(5,0)]
	piece.rooks = [makeposition(0,0), makeposition(7,0)]
	piece.knights = [makeposition(1,0), makeposition(6,0)]
	piece.queens = [makeposition(4,0)]
	piece.king = [makeposition(3,0)]
	return piece

#this class contains all pieces black and white
class allPieces(object):
	black = blackPieces()
	white = whitePieces()

#this class contains all pieces black and white, but pieces remain uninitialized here.  
class emptyPieces1(object):
	black = returnpieces()
	white = returnpieces()

#this function returns an instance of empty pieces
def initemptypieces1():
	ps = emptyPieces1()
	ps.black = returnpieces()
	ps.white = returnpieces()
	return ps

#this function returns an instance of player1
def makep1():
	p1 = Player1()
	return p1

#this function returns an instance of player2
def makep2():
	p2 = Player2()
	return p2

def makeallpieces():
	allp = allPieces()
	return allp

#this class defines the gamestructure
class Gamestructure(object):
	playerone = makep1()
	playertwo = makep2()
	current = 1
	allpieces = allPieces()
	
	playerone.pieces = Pieces()
	playertwo.pieces = Pieces()

	currentplayer = playerone
	otherplayer = playertwo

#this function creates and returns a gamestructure instance
def makeGamestructure(status, p1type, p2type):
	gs = Gamestructure()
	gs.playerone = makep1()
	gs.playertwo = makep2()
	gs.allpieces = makeallpieces()
	if p1type is 0:
		gs.playerone.playertype = 0
	else:
		gs.playerone.playertype = 1
		
	if p2type is 0:
		gs.playertwo.playertype = 0
	else:
		gs.playertwo.playertype = 1


	if status is 1:
		gs.playerone.pieces = gs.allpieces.white
		gs.playertwo.pieces = gs.allpieces.black
		gs.playertwo.color = "B"
		gs.currentplayer = gs.playerone
		gs.otherplayer = gs.playertwo
		current = 1
	else:
		gs.playerone.pieces = gs.allpieces.black
		gs.playertwo.pieces = gs.allpieces.white
		gs.currentplayer = gs.playertwo
		gs.playerone.color = "B"
		gs.otherplayer = gs.playerone
		gs.current = 2
	return gs

#this class defines an emptygamestructure
class emptyGamestructure(object):
	playerone = Player1()
	playertwo = Player2()
	current = 1
	allpieces = initemptypieces1()
	randarr = []	
	playerone.pieces = allpieces.white
	playertwo.pieces = allpieces.black

	currentplayer = playerone
	otherplayer = playertwo
	
#this function creates and returns an empty gamestructure instance	
def makeemptyGamestructure():
	gs = emptyGamestructure()
	gs.playerone = makep1()
	gs.playertwo = makep2()
	gs.current = 1
	gs.allpieces = initemptypieces1()
	gs.randarr = []
	gs.playerone.pieces = emptyPieces1()
	gs.playertwo.pieces = emptyPieces1()

	gs.currentplayer = gs.playerone
	gs.otherplayer = gs.playertwo
	return gs

#this class defines a move, which has a start and end position, a piece to move, and a move validity flag
class Move(object):
	position1 = Position()
	position2 = Position()
	piece = ""
	valid = 0

#this function creates and returns a move
def createmove(p, p1, p2):
	mv = Move()
	mv.position1 = p1
	mv.position2 = p2
	mv.piece = p
	return mv