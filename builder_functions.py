#############################################################
##Name: Taylor Del Matto
##Course: CS 419
##Final Project: Chess Game
##builderfunctions
##Description: These functions are used to build the more complex functions
## in primary functions.  
#############################################################
import random
import copy
import sys, os
from gamestructure import *

#this function blocks printing to the console window
def blockPrint():
	sys.stdout = open(os.devnull, 'w')

#this function unblocks printing to the console window
def enablePrint():
	sys.stdout = sys.__stdout__
	
#getpiece
#
#this function takes a positionobject and returns the piece or lack of piece at that position
#on the chessarray

def getpiecefrompos(chessarray1, position2):
	return chessarray1[position2.y][position2.x]

#this function prints a position
def printPosition(position1, chessarray):
	print "piece is"
	print getpiecefrompos(chessarray, position1)
	print "x,y is"
	print position1.x
	print position1.y	
	
#Print board function
#this function prints the chessboard
#
#---------------------------------------------------------
#|******|      |******|      |******|      |******|      |
#|**WR**|   W& |**WB**|  WK  |**WQ**|  WB  |**W&**|  WR  |
#|******|      |******|      |******|      |******|      |
#---------------------------------------------------------
#|      |******|      |******|      |******|      |******|  
#|  WP  |**WP**|  WP  |**WP**|  WP  |**WP**|  WP  |**WP**|  
#|      |******|      |******|      |******|      |******|    
#---------------------------------------------------------
#|******|      |******|      |******|      |******|      |
#|******|      |******|      |******|      |******|      |
#|******|      |******|      |******|      |******|      |
#---------------------------------------------------------
#|      |******|      |******|      |******|      |******|  
#|      |******|      |******|      |******|      |******|  
#|      |******|      |******|      |******|      |******|    
#---------------------------------------------------------
#|******|      |******|      |******|      |******|      |
#|******|      |******|      |******|      |******|      |
#|******|      |******|      |******|      |******|      |
#---------------------------------------------------------
#|      |******|      |******|      |******|      |******|  
#|      |******|      |******|      |******|      |******|  
#|      |******|      |******|      |******|      |******|    
#---------------------------------------------------------
#|******|      |******|      |******|      |******|      |
#|**BP**|  BP  |**BP**|  BP  |**BP**|  BP  |**BP**|  BP  |
#|******|      |******|      |******|      |******|      |
#---------------------------------------------------------
#|      |******|      |******|      |******|      |******|  
#|  BR  |**B&**|   BB |**BK**|  BQ  |**BB**|  B&  |**BR**|  
#|      |******|      |******|      |******|      |******|    
#---------------------------------------------------------
def printboard(chessarray):#either take chessboard as parameter or make global variable
	print "    A      B      C      D      E      F      G      H   "   

	#for each row r in chessboard matrix
	for x, row in enumerate(chessarray):
		print " --------------------------------------------------------"
		if x % 2 is 0: #if row is odd
			print " |******|      |******|      |******|      |******|      |"
		elif x % 2 == 1: #if row is even 
			print " |      |******|      |******|      |******|      |******|"		
		
		astring = str(x+1)
		for y, column in enumerate(row):
			#astring = str(x)
			if (x+y) % 2 is 0:
				astring = astring + "|**"
			elif (x+y) % 2 is 1:
				astring = astring + "|  "  
			if column != "0":	
				astring = astring + column 
			else:
				if (x+y) % 2 is 0:
					astring = astring + "**"
				elif (x+y) % 2 is 1:
					astring = astring + "  "  
		
			
			if (x+y) % 2 is 0:
				astring = astring + "**"
			elif (x+y) % 2 is 1:
				astring = astring + "  "    
		astring = astring + "|"
 		print astring
		if x % 2 is 0: #if row is odd
			print " |******|      |******|      |******|      |******|      |"
		elif x % 2 == 1: #if row is even 
			print " |      |******|      |******|      |******|      |******|"		

	print " --------------------------------------------------------"
	
	
#positiontoorderedpair
#
#this function converts the position i.e B5 into 2,5 which is 
#the indices of referenced spot in the chessarray by converting ascii
#letters a-h into numbers 1-8

def positiontoorderedpair(positionstring):
	position = Position()
	if ord(positionstring[0]) >= 65 and  ord(positionstring[0]) <= 74:
		position.x =  (ord(positionstring[0]) - 65)
		
	elif  ord(positionstring[0]) >= 97 and  ord(positionstring[0]) <= 108:
		position.x =  (ord(positionstring[0]) - 97)
	#else:
	 	#print "position is invalid"

	if ord(positionstring[1]) >= 48 and ord(positionstring[1]) <= 57:
		position.y = (ord(positionstring[1]) - 49)
	#else:
		#print "position is invalid"
	#print position.x
	#print position.y
	return position
	
	
#isvalidpawn
#
#this function determines if a pawn move is valid
#if currentplayer is 0 #current player is white then all possible moves would be positive

def isvalidpawn(move, chessarray, gamestructure):
	if move.piece[0] == 'W':
		m = 1 
	else:
		m = -1
			
	#currentplayer = getcurrentplayer(gamestructure)
	#otherplayer = getotherplayer(gamestructure)
	if issamecolor(gamestructure.currentplayer, move.piece):
		currentp = gamestructure.currentplayer
		otherp = gamestructure.otherplayer
	else:
		currentp = gamestructure.otherplayer
		otherp = gamestructure.currentplayer

	#print "enpassant bool vals"
	#print (move.position1.y + m*1) is move.position2.y 
	#print ((move.position1.x is (move.position2.x +1)) or (move.position1.x is (move.position2.x -1))) 
	#print (getpiecefrompos(chessarray, move.position2) == "0") 
	#print (len(currentp.enpassantvalid) > 0)
	
	
	#if square is one ahead and if no piece is in that position 
	if ((move.position1.y + m*1) is move.position2.y) and (move.position1.x is move.position2.x) and (getpiecefrompos(chessarray, move.position2) == "0"):
		move.valid = 1
		#if move.position2.y is 7 or move.position2.y is 0:
		#	player.pawnpflag = 1
		return 1
	#if square is two ahead and if no piece is in that position
	elif ((move.position1.y + m*2) is move.position2.y) and (move.position1.x is move.position2.x) and (getpiecefrompos(chessarray, move.position2)) == "0"and (getpiecefrompos(chessarray, makeposition(move.position2.x, (move.position2.y-(m*1)))) == "0") and (move.position1.y is 1 or move.position1.y is 6):
		
		
		#check if enpassant is valid for other player
		#get positions to left and right of pawn
		aposition1 = makeposition((move.position2.x -1), move.position2.y)
		aposition2 = makeposition((move.position2.x +1), move.position2.y)
		
		#if pieces are not the same color, and it is a pawn
		if(aposition1.x < 8 and aposition1.x >= 0):
			if getpiecefrompos(chessarray, aposition1) != "0":
				if(getpiecefrompos(chessarray, aposition1)[0] != move.piece[0] and getpiecefrompos(chessarray, aposition1)[1] == 'P'):
					#print "en passant potentially valid for"
					#print otherp.color
					otherp.enpassantvalid.append(move.position2)
	
		if(aposition2.x < 8 and aposition2.x >= 0):
			if getpiecefrompos(chessarray, aposition2) != "0":	
				if(getpiecefrompos(chessarray, aposition2)[0] != move.piece[0] and getpiecefrompos(chessarray, aposition2)[1] == 'P'):
					#print "en passant potentially valid for"
					#print otherp.color
					otherp.enpassantvalid.append(move.position2)
					
		#ADD THIS LATER-add piece to pieces taken list
		move.valid = 1
		return 1

	#if square is one ahead and one to the side and there is a piece at that position
	elif ((move.position1.y + m*1) is move.position2.y) and ((move.position1.x is (move.position2.x +1)) or (move.position1.x is (move.position2.x -1))) and (getpiecefrompos(chessarray, move.position2) != "0"):
		move.valid = 1
		
		#if move.position2.y is 7 or move.position2.y is 0:
		#	player.pawnpflag = 1
		return 1
		#if there is a pawn to the left or to the right of position2 such that that pawn is the opposite color of the currentplayer
			#set en passant flag for opposing player
	
	#check for enpassant current player
	elif ((move.position1.y + m*1) is move.position2.y) and ((move.position1.x is (move.position2.x +1)) or (move.position1.x is (move.position2.x -1))) and (getpiecefrompos(chessarray, move.position2) == "0") and (len(currentp.enpassantvalid) > 0):
		#print "first en if passed"
		for x1, positiona in enumerate(currentp.enpassantvalid):
			#print "second en if passed"
			#if move is to left and positiona is to left
			#print "move, positiona"
			#print move.position1.x
			#print move.position1.y
			#print move.position2.x
			#print move.position2.y
			#print positiona.x
			#print positiona.y

			if(move.position1.y is positiona.y and move.position2.x is positiona.x):		
				#then enpassant is good
				#print "enpassant movevalid for"
				#print currentp.color
				move.valid = 1
				return 1
			#if move is to left and positiona is to left
				#then enpassant is good
				#move.valid = 1
				#return 1	 
	 	
			
	
	#elif posityion1.y + 1 is position2.y and getpiece(move.position2 != 0 and (position1.x - 1 is position2.x or position1.x +1 is position2.x) 

	print "Invalid move: pawn move invalid, try again"
	return 0

#this function checks if a knight move is valid	
def isvalidknight(move, chessarray, gamestructure):
	#print "isvalidknight triggered"
	if ((((move.position1.y + 2) is move.position2.y) or ((move.position1.y - 2) is move.position2.y))  and ((move.position1.x is move.position2.x+ 1) or (move.position1.x is move.position2.x - 1))) or ((((move.position1.x + 2) is move.position2.x) or ((move.position1.x - 2) is move.position2.x))  and ((move.position1.y is move.position2.y+ 1) or (move.position1.y is move.position2.y - 1))):
		move.valid = 1
		return 1
	else:
		print "Invalid move: knight move invalid"
		return 0

#this function checks if a bishop move is valid
def isvalidbishop(move, chessarray, gamestructure):
	#print "isvalid bishop called"
	#check that an actual move has been entered
	if(move.position1.y is move.position2.y and move.position2.x is move.position1.x):
		print "ERROR, Bishop currently occupies that space, try a different move"
		return 0
		
	if (move.position1.y - move.position2.y) is (move.position1.x - move.position2.x):
		if move.position2.x > move.position1.x:
			m = 1
		else:
			m = -1
		
		y = move.position1.y + m
		x = move.position1.x + m
		while (x * m) < (move.position2.x * m): 
			if(x > 7 or x < 0 or y > 7 or y < 0):
				print "Invalid move: isvalid bishop game logic error, you should not see this!"
				return 0
			if getpiecefrompos(chessarray, makeposition(x,y)) != "0":
				print "Invalid move: that move is blocked! please try a different move"
				return 0
			#increment
			x =  x + m
			y = y + m
		move.valid = 1
		#print "bishop returned 1"
		return 1
			
	elif (move.position1.y - move.position2.y) is (-1 * (move.position1.x - move.position2.x)):
		#note the nested if for the above if actually effectively tests the same thing, just 
		#a different mathematical approach
		if (move.position2.x - move.position1.x) > 0:
			m = 1
		else:
			m = -1
		
		y = move.position1.y + (m * -1)
		x = move.position1.x + m
		while (x * m) < (move.position2.x * m): 
			if(x > 7 or x < 0 or y > 7 or y < 0):
				print "Invalid move: isvalid bishop game logic error, you should not see this!"
				return 0
			if getpiecefrompos(chessarray, makeposition(x,y)) != "0":
				print "Invalid move: that move is blocked! please try a different move"
				return 0
			#increment
			x =  x + m
			y = y + (m * -1)
		move.valid = 1
		#print "bishop returned 1"
		return 1
	else:
		print "Invalid Move: bishop move invalid!"
		return 0
			
			
#this function checks if a rook move is valid
def isvalidrook(move, chessarray, gamestructure):
	if (move.position1.x is move.position2.x):
		if (move.position2.y - move.position1.y) > 0:
			m = 1
		else:
			m = -1
		x = move.position1.x
		y = move.position1.y + m
		while (y*m) < (move.position2.y * m):
			if(x > 7 or x < 0 or y > 7 or y < 0):
				print "Invalid move: isvalid bishop game logic error, you should not see this!"
				return 0
			if getpiecefrompos(chessarray, makeposition(x,y)) != "0":
				print "Invalid move: that move is blocked! please try a different move"
				return 0
			y = y + m
		move.valid = 1
		return 1
	elif move.position1.y is move.position2.y:
		if (move.position2.x - move.position1.x) > 0:
			m = 1
		else:
			m = -1
		y = move.position1.y
		x = move.position1.x + m
		while (x*m) < (move.position2.x * m):
			if(x > 7 or x < 0 or y > 7 or y < 0):
				print "Invalid move: isvalid bishop game logic error, you should not see this!"
				return 0
			if getpiecefrompos(chessarray, makeposition(x,y)) != "0":
				print "Invalid move: that move is blocked! please try a different move"
				return 0
			x = x + m
		move.valid = 1
		return 1

#this function checks if a queen move is valid
def isvalidqueen(move, chessarray, gamestructure):
	#introduce isqueeen flag as a parameter for these functions for later
	return (isvalidrook(move,chessarray, gamestructure) or isvalidbishop(move, chessarray, gamestructure))	

#this function checks if a king move is valid
def isvalidking(move, chessarray, gamestructure):
	if issamecolor(gamestructure.currentplayer, move.piece):
		currentp = gamestructure.currentplayer
		otherp = gamestructure.otherplayer
	else:
		currentp = gamestructure.otherplayer
		otherp = gamestructure.currentplayer
	
	m = (move.position2.x - move.position1.x) / 2

	if abs(move.position2.y - move.position1.y) <= 1 and abs(move.position2.x - move.position1.x) <=1:
		move.valid = 1
		return 1
	#elif castle is valid
	#conditions: king moves two spaces right or left, hrook has not been moved, arook has not been moved,
	#conditions continued: king has not been moved, both spaces covered by king are not covered by any opposing piece
	#conditions continued: the king is not in check,
	
		#elif 1:
	elif (move.position1.y is move.position2.y) and ((move.position1.x is (move.position2.x + 2)) or (move.position1.x is (move.position2.x - 2))) and ((currentp.hrookmoved is 0 and m < 0)  or (currentp.arookmoved is 0 and m > 0)) and currentp.kingmoved is 0:
		p1 = makeposition((move.position1.x + m), move.position1.y)
		p2 = makeposition(move.position2.x, move.position2.y)
		p3 = makeposition((move.position2.x + m), move.position1.y)	
		
		if isplacecoveredfortake(chessarray, gamestructure, otherp, p1, 0) is 0 and isplacecoveredfortake(chessarray, gamestructure, otherp, p2, 0) is 0 and (getpiecefrompos(chessarray, p1) == '0') and (getpiecefrompos(chessarray, p2) == '0') and (m < 0 or (getpiecefrompos(chessarray, p3) == '0')) and currentp.checkflag is 0: 
			print "castle valid"
			move.valid = 1
			currentp.castleflag = 1	
			return 1
		print "Castle Move invalid!"
		return 0
	else:
		print "Invalid Move: Please try again!"
		return 0

#this function checks if a position is in bounds
def ispositioninbounds(position):
	if position.x > 7 or position.y > 7 or position.x < 0 or position.y < 0: 
		return 0
	return 1

#this function returns the current player
def getcurrentplayer(gamestructure):
	if gamestructure.current is 1:
		return gamestructure.playerone
	elif gamestructure.current is 2:
		return gamestructure.playertwo
	else:
		print "error, this should not display, game logic error in get current player"

#this function returns the non current player
def getotherplayer(gamestructure):
	if gamestructure.current is 1:
		return gamestructure.playertwo
	elif gamestructure.current is 2:
		return gamestructure.playerone
	else:
		print "error, this should not display, game logic error in get other player"

#this function copies the gamestate
def copygamestate(gamestructure):
	teststructure = makeemptyGamestructure()
	teststructure.allpieces.white.pawns = []
	#if gamestructure.allpieces.white.pawns == []:
		#print "equates to a problem"
	#else:
		#print " no problem"

	#teststructure.allpieces = copy.deepcopy(gamestructure.allpieces)
	for x, arr in enumerate(gamestructure.allpieces.white.pawns):
		teststructure.allpieces.white.pawns.append(makeposition(arr.x, arr.y))

	#teststructure.allpieces.white.pawns = gamestructure.allpieces.white.pawns[:]
	teststructure.allpieces.white.rooks = gamestructure.allpieces.white.rooks[:]
	teststructure.allpieces.white.knights = gamestructure.allpieces.white.knights[:]
	teststructure.allpieces.white.bishops = gamestructure.allpieces.white.bishops[:]
	teststructure.allpieces.white.queens = gamestructure.allpieces.white.queens[:]
	teststructure.allpieces.white.king = gamestructure.allpieces.white.king[:]

	teststructure.allpieces.black.pawns = gamestructure.allpieces.black.pawns[:]
	teststructure.allpieces.black.rooks = gamestructure.allpieces.black.rooks[:]
	teststructure.allpieces.black.knights = gamestructure.allpieces.black.knights[:]
	teststructure.allpieces.black.bishops = gamestructure.allpieces.black.bishops[:]
	teststructure.allpieces.black.queens = gamestructure.allpieces.black.queens[:]
	teststructure.allpieces.black.king = gamestructure.allpieces.black.king[:]
	
	teststructure.playerone.castleflag = gamestructure.playerone.castleflag
	teststructure.playerone.pawnpflag = gamestructure.playerone.pawnpflag
	teststructure.playerone.enpassantvalid = gamestructure.playerone.enpassantvalid[:]
	teststructure.playerone.checkflag = gamestructure.playerone.checkflag
	teststructure.playerone.playertype = gamestructure.playerone.playertype
	teststructure.playerone.hrookmoved = gamestructure.playerone.hrookmoved
	teststructure.playerone.arookmoved = gamestructure.playerone.arookmoved
	teststructure.playerone.kingmoved =  gamestructure.playerone.kingmoved
	teststructure.playerone.color = gamestructure.playerone.color[:]
	teststructure.playerone.piecestaken = gamestructure.playerone.piecestaken[:]

	teststructure.playertwo.castleflag = gamestructure.playertwo.castleflag
	teststructure.playertwo.pawnpflag = gamestructure.playertwo.pawnpflag
	teststructure.playertwo.enpassantvalid = gamestructure.playertwo.enpassantvalid[:]
	teststructure.playertwo.checkflag = gamestructure.playertwo.checkflag
	teststructure.playertwo.playertype = gamestructure.playertwo.playertype
	teststructure.playertwo.hrookmoved = gamestructure.playertwo.hrookmoved
	teststructure.playertwo.arookmoved = gamestructure.playertwo.arookmoved
	teststructure.playertwo.kingmoved =  gamestructure.playertwo.kingmoved
	teststructure.playertwo.color = gamestructure.playertwo.color[:]
	teststructure.playertwo.piecestaken = gamestructure.playertwo.piecestaken[:]

	if(gamestructure.playerone.pieces is gamestructure.allpieces.black):
		teststructure.playerone.pieces = teststructure.allpieces.black
		teststructure.playertwo.pieces = teststructure.allpieces.white
	elif(gamestructure.playerone.pieces is gamestructure.allpieces.white):
		teststructure.playerone.pieces = teststructure.allpieces.white
		teststructure.playertwo.pieces = teststructure.allpieces.black
	else:
		print "gamelogic error gs copy"
	
	if(gamestructure.playerone is gamestructure.currentplayer):
		teststructure.currentplayer = teststructure.playerone
		teststructure.otherplayer = teststructure.playertwo
		teststructure.current = 1
	elif gamestructure.playerone is gamestructure.otherplayer:	
		teststructure.currentplayer = teststructure.playertwo
		teststructure.otherplayer = teststructure.playerone
		teststructure.current = 2
	else:
		print "game logic  error, in gamestructure copy"
	
	return teststructure
	
#this function prints the position list of all pieces
def printplist(move, gamestructure):
	for piece in gamestructure.allpieces.black.pawns:
		print "piece"
		print piece.x
		print piece.y
		print "   "
			

#this function moves a piece in the chessarray data structure
def movepiece(gamestructure, chessarray, move):
	#if enpassant flag is set
		#move enpassant
	#elif castling flag is set
		#move castle
	#elif pawn promotion flag is set
		#get piece type from user
		#exchange pawn for correct piece
	#else
	if issamecolor(gamestructure.currentplayer, "WB"):
		white = gamestructure.currentplayer
		black = gamestructure.otherplayer
	else:
		black = gamestructure.currentplayer
		white = gamestructure.otherplayer	
	
	if issamecolor(gamestructure.currentplayer, move.piece):
		thisplayer = gamestructure.currentplayer
	else:
		thisplayer = gamestructure.otherplayer
	
	if move.piece[0] == 'W':
		m = 1
		apawnpiece = "BP" 
	else:
		m = -1
		apawnpiece = "WP"
	#if a pawn has been moved 2 spaces, and there is a pawn adjacent to it, enpassant valid for the other player for the adjacent pawn position
	#note you will need to change enpassantvalid to an empty list you will need to change this in the game structure
	if ((move.position1.y + m*1) is move.position2.y) and ((move.position1.x is (move.position2.x +1)) or (move.position1.x is (move.position2.x -1))) and (getpiecefrompos(chessarray, move.position2) == "0") and (len(thisplayer.enpassantvalid) > 0):	
		takepawnpos = makeposition(move.position2.x, move.position1.y)
		if getpiecefrompos(chessarray, takepawnpos) != apawnpiece:
			print "error, enpassant movepiece this shouldnt happen"
		else:
			#remove pawn in place from chessarray
			chessarray[takepawnpos.y][takepawnpos.x] = "0"
				
			#remove pawn in place from gamestructure
			removepieceplist(apawnpiece, takepawnpos, gamestructure)

			#move current pawn
			chessarray[move.position2.y][move.position2.x] = chessarray[move.position1.y][move.position1.x]
			chessarray[move.position1.y][move.position1.x] = '0'
			return	
	#else:
		#print "error enpassant movepiece, this shouldnt happen"

	if move.piece[1] == 'R' and (move.piece[0] == 'W' and ((move.position1.x is 0 or move.position1.x is 7) and move.position1.y is 0)) or (move.piece[0] == 'B' and ((move.position1.x is 0 or move.position1.x is 7) and move.position1.y is 7)):
		if move.piece[0] == 'W':
			print "a rook has been moved from its original position"
			if move.position1.x is 0:
				white.hrookmoved = 1	
			else:
				white.arookmoved = 1
		else:
			if move.position1.x is 0:
				black.hrookmoved = 1	
			else:
				black.arookmoved = 1	
	
	if move.piece[1] == 'K' and ((move.piece[0] == 'W' and (move.position1.x is 3 and  move.position1.y is 0)) or (move.piece[0] == 'B' and (move.position1.x is 3 and move.position1.y is 7))):
		#print "king moved from original position!"
		if move.piece[0] == 'W':
			white.kingmoved = 1
		else:
			black.kingmoved = 1
	
	#castle move
	if(thisplayer.castleflag is 1):
		chessarray[move.position2.y][move.position2.x] = chessarray[move.position1.y][move.position1.x]
		chessarray[move.position1.y][move.position1.x] = '0'
		apiece = gamestructure.currentplayer.color + "R"
		#aside rook
		if (move.position2.x - move.position1.x) > 0:
					xval = 7
					aposition1 = makeposition(xval, move.position1.y)
					aposition2 = makeposition((move.position2.x-1), move.position1.y)
					move2 = createmove(apiece, aposition1, aposition2)
					moveplist(move2, gamestructure)		
					#print "position1, position2 is"
					#printPosition(move2.position1, chessarray)
					#printPosition(move2.position2, chessarray)
					chessarray[move2.position2.y][move2.position2.x] = chessarray[move2.position1.y][move2.position1.x]
					chessarray[move2.position1.y][move2.position1.x] = '0'
		elif (move.position2.x - move.position1.x) < 0:
					xval = 0
					aposition1 = makeposition(xval, move.position1.y)
					aposition2 = makeposition((move.position2.x+1), move.position1.y)
					move2 = createmove(apiece, aposition1, aposition2)
					moveplist(move2, gamestructure)	
					#print "position1, position2 is"
					#printPosition(move2.position1, chessarray)
					#printPosition(move2.position2, chessarray)
	
					chessarray[move2.position2.y][move2.position2.x] = chessarray[move2.position1.y][move2.position1.x]
					chessarray[move2.position1.y][move2.position1.x] = '0'
		else:
			print "error movepiece castle you shouldnt see this"
		return

	apiece = getpiecefrompos(chessarray, move.position2) 
	if apiece != '0':
		removepieceplist(apiece, move.position2, gamestructure)
	chessarray[move.position2.y][move.position2.x] = chessarray[move.position1.y][move.position1.x]
	chessarray[move.position1.y][move.position1.x] = '0'

#this function removes a piece from the piece list data structure
def removepieceplist(piece, position, gamestructure):
	#print "in removeplist"
	#initialize mypieces 
	#mypieces = gamestructure.currentplayer.pieces
	if piece[0] == 'W':
		mypieces = gamestructure.allpieces.white
	else:
		mypieces = gamestructure.allpieces.black

	if piece[1] == 'P':
		pieces1 = mypieces.pawns
	elif piece[1] == '&':
		pieces1 = mypieces.knights
	elif piece[1] == 'B':
		pieces1 = mypieces.bishops
	elif piece[1] == 'R':
		pieces1 = mypieces.rooks
	elif piece[1] == 'Q':
		pieces1 = mypieces.queens
	elif piece[1] == 'K':
		pieces1 = mypieces.king
	else:
		print "game logic error in removepieceplist, this shouldnt happen"
	
	#find the piece with that position and change position to proper location	
	for i, pieceposition in enumerate(pieces1):
		if (pieceposition.x == position.x) and (pieceposition.y == position.y):
				del pieces1[i]
				#print "list change successful"
				return
	print "game logic error removepieceplist unsuccessful this shouldnt happen"	
				
#this function moves a piece in the position list
def moveplist(move, gnomestructure):
	#print "in moveplist"
	#initialize mypieces 
	#mypieces = gamestructure.currentplayer.pieces

	#the player using move plist could be the other player as in ischeckmate,
	#so the color of the pieces to be moved is dictated by the color of the
	#piece in the move object
	if move.piece[0] == 'W':
		mypieces = gnomestructure.allpieces.white
	else:
		mypieces = gnomestructure.allpieces.black
	
	if move.piece[1] == 'P':
		pieces1 = mypieces.pawns
	elif move.piece[1] == '&':
		pieces1 = mypieces.knights
	elif move.piece[1] == 'B':
		pieces1 = mypieces.bishops
	elif move.piece[1] == 'R':
		pieces1 = mypieces.rooks
	elif move.piece[1] == 'Q':
		pieces1 = mypieces.queens
	elif move.piece[1] == 'K':
		pieces1 = mypieces.king
	else:
		print "game logic error in moveplist, this shouldnt happen"

	
	#find the piece with that position and change position to proper location	
	for i, pieceposition in enumerate(pieces1):
		#print "pieceposition is"
		#print pieceposition.x
		#print pieceposition.y
		#print "moveposition is"
		#print move.position1.x
		#print move.position1.y
		if (pieceposition.x == move.position1.x) and (pieceposition.y == move.position1.y):
				pieces1[i] = makeposition(move.position2.x, move.position2.y)
				#print "list change successful"
				return
	print "game logic error move plist unsuccessful this shouldnt happen"

#this function checks to see if a player and a piece are of the same color.  
def issamecolor(player, piece):
	if(player.color[0] == piece[0]):
		return 1
	else:
		return 0	
