#############################################################
##Name: Taylor Del Matto
##Course: CS 419
##Final Project: Chess Game
##primaryfunctions
##Description: These functions are the main game play functions.
#############################################################
import random
import copy
import sys, os
from gamestructure import *
from  builder_functions import *

#getmove
#this function gets a move from the player or computer
def getmove(gamestructure1, chessarray, exitflag1):
	if gamestructure1.currentplayer.playertype is 0: #HUMAN
		#get command line input
		validmove = 0
		while validmove is 0:
			if gamestructure1.currentplayer is gamestructure1.playerone:
				print "Player One it is your turn"
			else: 
				print "Player Two it is your turn"
			printboard(chessarray)
			input1 = raw_input("enter your move ")
			#print ("input1 is %s" %  (input1))
			inargs =  input1.split()
			#piece = inargs[0]
			#print len(inargs)
			if len(inargs) is 2:
	
				if len(inargs[0]) is 2 and len(inargs[1]) is 2:	
					position1 = positiontoorderedpair(inargs[0])
					position2 = positiontoorderedpair(inargs[1])		
					if position1.x > 7 or position1.y > 7 or position2.x > 7 or position2.y > 7 or position1.x < 0 or position1.y < 0 or position2.x < 0 or position2.y < 0:
						print "invalid move: position entered does not exist"
					else:
						piece = getpiecefrompos(chessarray, position1)
						if piece != '0':
							validmove = 1
						else:
							print "Invalid move: no piece exists at that position"
				else:
					print "Invalid move: arguments must be two characters long"
					print "Move format takes 2 arguments: startposition endposition"
					print "Example:"
					print "a3 a4"

			
			elif inargs[0] == "exit":
				print "EXIT!"
				exitflag1 = 1
				Move = createmove(piece, Position(), Position())
				return Move, exitflag1
			else:
				print "invalid move and/or arguments"
				print "Move format takes 2 arguments: startposition endposition"
				print "Example:"
				print "a3 a4"
					
		#print ("piece is 0%s0" % (piece))
		Move = createmove(piece, position1, position2)
		return Move, exitflag1
	elif gamestructure1.currentplayer.playertype is 1: #computer
		#print "insert computer move here"
		#return calculatecomputermove(), 0
		#don't move if you can't move
                #print "computer moves"
		blockPrint()
                move, num = AlphaBetaMax(-999999, 999999, 2)
                enablePrint()
                #print "move returned"
                if isvalid(move, chessarray2, gamestate2) == 0:
                    print "this should never happen"
                    print move.piece
                    print move.position1.x
                    print move.position1.y
                    print move.position2.x
                    print move.position2.y
                    printboard(chesslist)
                    print "computer forfited"
                    c.execute("UPDATE Users SET wins=wins+1 WHERE name ='" + logInName + "';")
                    conn.commit()
                    conn.close() 
                    sys.exit()
		#return calculatecomputermove(), 0
                return move, exitflag1


		#createmove from computermovecalculate(chessarray)
		#return move
	#else 
		#error!!!!!






#isvalid
#
#this function takes a move object and tests that move to see if it is valid
#if the move is invalid, the move.valid property is changed to 0
#if the move is a valid castle, pawn promotion, or enpassant, the respective flag is set
#so that the movepiece function can make the correct special move

def isvalid(move1, chessarray, gamestructure):
	#set player
	if gamestructure.current is 1:
		#print "current player is playerone"
		player = gamestructure.playerone
	else:
		#print "current player is playertwo"
		player = gamestructure.playertwo
	
	if move1.position1.x > 7 or move1.position1.y > 7 or move1.position2.x > 7 or move1.position2.y > 7 or move1.position1.x < 0 or move1.position1.y < 0 or move1.position2.x < 0 or move1.position2.y < 0:
		print "invalid move: position entered does not exist"
		return 0
	#preliminary validity checks	
	elif getpiecefrompos(chessarray, move1.position1) != move1.piece:
		print "invalid move: piece entered does not match piece at that location"
		return 0
	elif move1.position1.x is move1.position2.x and move1.position1.y is move1.position2.y:
		print "invalid move: no valid move entered"
		return 0
	elif getpiecefrompos(chessarray, move1.position1)[0] != player.color[0]:
		#print getpiecefrompos(chessarray, move1.position1)[0]
		#print player.color[0]
		print "invalid move: wrong piece! that piece is not your color."
		return 0
	elif getpiecefrompos(chessarray, move1.position2)[0] == player.color[0]:
		print "invalid move: you cannot take a piecethat is not your color."
		return 0
	
	#elif player.checkflag is 1 and move1.piece[1] != 'K': #then move is not valid!!!
	#	print "Invalid Move: your are in check and must move your king"
	#	return 0
	elif ismoveintocheck(move1, chessarray, gamestructure):
		print "Invalid Move: you are moving into check!"
		return 0
	
	if move1.piece[1] == 'P':
		return isvalidpawn(move1, chessarray, gamestructure)
	elif(move1.piece[1] == '&'):
		return isvalidknight(move1, chessarray, gamestructure)
	elif(move1.piece[1] == 'B'):
		return isvalidbishop(move1, chessarray, gamestructure)
	elif(move1.piece[1] == 'R'):
		return isvalidrook(move1, chessarray, gamestructure)
	elif(move1.piece[1] == 'Q'):
		return isvalidqueen(move1, chessarray, gamestructure)
	elif(move1.piece[1] == 'K'):
		return isvalidking(move1, chessarray, gamestructure)
	else:
		print "piece invalid this should not happen, game logic error"
		return 0

	#move1.valid = 1 #REMOVE THIS LATER WILL MAKE ALL MOVES VALID UNLESS STOPPED IN PRELIMINARY CHECK BLOCK
	return



#ismoveintocheck
#
#this function checks if the current move moves the player into check and is therefore illegal
def ismoveintocheck(move, chessarray, gamestructure):
	#print "in ismoveintocheck"
	#getplayers
	currentplayer = gamestructure.currentplayer
	otherplayer = gamestructure.otherplayer

	
	#create copies of chessarray and gamestructure to pass to isvalidpiece functions
	testarray = copy.deepcopy(chessarray)
	teststructure = copygamestate(gamestructure)
	#teststructure = emptyGamestructure()
	
	#if(teststructure.current is 1):
	#	teststructure.current = 2
	#else:
	#	teststructure.current = 1
	#implement move in testarray
	movepiece(teststructure, testarray, move)
	#print "moveplist test structure"
	
	#NOTE: FOR SOME REASON moveplist is not working here, perhaps this has  something to do with deep copy

	moveplist(move, teststructure)
	#print "king.y is "
	#print teststructure.currentplayer.pieces.king[0].y 
	
	if move.piece[0] == 'B':
		otherpieces = teststructure.allpieces.white
		mypieces = teststructure.allpieces.black
	else:
		#print "this is what happens if you are white"
		otherpieces = teststructure.allpieces.black
		mypieces = teststructure.allpieces.white


	if move.piece[0] == 'B':
		kingpos = teststructure.allpieces.black.king[0]	
	else:
		kingpos = teststructure.allpieces.white.king[0]

	#print "this is testarray"
	#printboard(testarray)
	blockPrint()
	for position in otherpieces.pawns:
		#if that piece can move to your king position, then you are in check
		newmove = createmove(getpiecefrompos(testarray , position), position, kingpos)
		if isvalidpawn(newmove, testarray, teststructure):
			enablePrint()
			print "an opposing pawn covers that square!"
			return 1
	for position in otherpieces.knights:
		#if that piece can move to your king position, then you are in check
		newmove = createmove(getpiecefrompos(testarray, position), position, kingpos)
		if isvalidknight(newmove, testarray, teststructure):
			enablePrint()
			print "an opposing knight will attack the king!"			
			return 1
	for position in otherpieces.bishops:
		#print "bishops loop happened"
		#if that piece can move to your king position, then you are in check
		newmove = createmove(getpiecefrompos(testarray, position), position, kingpos)
		if isvalidbishop(newmove, testarray, teststructure) == 1:
			enablePrint()
			print "an opposing bishop will attack the king!"
			#print "start print test array"
			#printboard(testarray)
			#print "end print testarray"
			return 1
	for position in otherpieces.rooks:
		#if that piece can move to your king position, then you are in check
		newmove = createmove(getpiecefrompos(testarray, position), position, kingpos)
		if isvalidrook(newmove, testarray, teststructure):
			enablePrint()
			print "an opposing rook will attack the king!"
			return 1

	for position in otherpieces.queens:
		#if that piece can move to your king position, then you are in check
		newmove = createmove(getpiecefrompos(testarray, position), position, kingpos)
		if isvalidqueen(newmove, testarray, teststructure):
			enablePrint()
			print "an opposing queen will attack the king!"
			return 1
	for position in otherpieces.king:
		#if that piece can move to your king position, then you are in check
		newmove = createmove(getpiecefrompos(testarray, position), position, kingpos)
		if isvalidking(newmove, testarray, teststructure):
			enablePrint()
			print "The opposing king covers that square!"
			return 1
	enablePrint()
	return 0

#isplacecoveredfortake
#
#this function checks for coverage like the original isplace covered function
#except that a pawn covers a space if it can take a piece on that space opposed to if 
#it can move there right now
def isplacecoveredfortake(chessarray, gamestructure, attackerplayer, posin, getparrayflag):
	#getplayerswritten
	#currentplayer = getcurrentplayer(gamestructure)
	#otherplayer = getotherplayer(gamestructure)
	if issamecolor(attackerplayer, "W"):
		attackerpieces = gamestructure.allpieces.white
		atttackedpieces = gamestructure.allpieces.black

	else:
		#print "this is what happens if you are white"by
		attackerpieces = gamestructure.allpieces.black
		attackedpieces = gamestructure.allpieces.white
	
	if posin.x > 7 or posin.y > 7 or posin.x < 0 or posin.y < 0:
		print "invalid move: position entered does not exist"
		return 2
	
	positions = []
	#print "this is testarray"T
	#printboard(testarray)K
	blockPrint()
	for position in attackerpieces.pawns:
		#if that piece can move to position, then that place iscovered
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		
		if newmove.piece[0] == 'W':
			m = 1 
		else:
			m = -1

	
		#if square is one ahead and one to the side and there is a piece at that position
		if ((newmove.position1.y + m*1) is newmove.position2.y) and ((newmove.position1.x is (newmove.position2.x +1)) or (newmove.position1.x is (newmove.position2.x -1))) :
			enablePrint()
			#print "covered by pawn!"
			
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.knights:
		#if that piece can move to position, then that place iscovered
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidknight(newmove, chessarray, gamestructure):
			enablePrint()
			#print "CHECK!"			
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.bishops:
		#print "bishops loop happened"
		#if that piece can move to posin, it is coverd by attacker
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidbishop(newmove, chessarray, gamestructure) == 1:
			enablePrint()
			#print "CHECK!"
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.rooks:
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidrook(newmove, chessarray, gamestructure):
			enablePrint()
			#print "CHECK!"
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)


	for position in attackerpieces.queens:
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidqueen(newmove, chessarray, gamestructure):
			enablePrint()
			#print "CHECK!"
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.king:
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidking(newmove, chessarray, gamestructure):
			enablePrint()
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	enablePrint()
	if(getparrayflag is 0):
		return 0
	if(len(positions) >= 1 and getparrayflag is 1):
		return 1, positions
	
	elif len(positions) is 0 and getparrayflag is 1:
		return 0, positions 
	else:
		print "this shouldnt happen, game logic error"
				
#ismoveintocheck
#
#this function checks to see if the attackerplayer covers the positionin.  
def isplacecovered(chessarray, gamestructure, attackerplayer, posin, getparrayflag):
	#getplayerswritten
	#currentplayer = getcurrentplayer(gamestructure)
	#otherplayer = getotherplayer(gamestructure)
	if issamecolor(attackerplayer, "W"):
		attackerpieces = gamestructure.allpieces.white
		atttackedpieces = gamestructure.allpieces.black

	else:
		#print "this is what happens if you are white"by
		attackerpieces = gamestructure.allpieces.black
		attackedpieces = gamestructure.allpieces.white
	
	if posin.x > 7 or posin.y > 7 or posin.x < 0 or posin.y < 0:
		print "invalid move: position entered does not exist"
		return 2
	
	positions = []
	#print "this is testarray"T
	#printboard(testarray)K
	blockPrint()
	for position in attackerpieces.pawns:
		#if that piece can move to position, then that place iscovered
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidpawn(newmove, chessarray, gamestructure):
			enablePrint()
			#print "covered by pawn!"
			
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)
	
	for position in attackerpieces.knights:
		#if that piece can move to position, then that place iscovered
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidknight(newmove, chessarray, gamestructure):
			enablePrint()
			#print "CHECK!"			
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.bishops:
		#print "bishops loop happened"
		#if that piece can move to posin, it is coverd by attacker
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidbishop(newmove, chessarray, gamestructure) == 1:
			enablePrint()
			#print "CHECK!"
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.rooks:
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidrook(newmove, chessarray, gamestructure):
			enablePrint()
			#print "CHECK!"
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)


	for position in attackerpieces.queens:
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidqueen(newmove, chessarray, gamestructure):
			enablePrint()
			#print "CHECK!"
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	for position in attackerpieces.king:
		newmove = createmove(getpiecefrompos(chessarray, position), position, posin)
		if isvalidking(newmove, chessarray, gamestructure):
			enablePrint()
			#if no get position array return 1
			if getparrayflag is 0:
				return 1
			else:
				positions.append(newmove.position1)

	enablePrint()
	if(getparrayflag is 0):
		return 0
	if(len(positions) >= 1 and getparrayflag is 1):
		return 1, positions
	
	elif len(positions) is 0 and getparrayflag is 1:
		return 0, positions 
	else:
		print "this shouldnt happen, game logic error"

#this function checks a move to see if it is blockable
def ismoveblockable(move, chessarray, gamestructure, blockme, blocker):
	#for piece type
	if move.piece[1] == 'P':
		return 0
	elif move.piece[1] == '&':
		return 0
	elif move.piece[1] == 'B':
		#pieces1 = blocker.bishops
		#print "isvalid bishop called"
		#check that an actual move has been entered
		if(move.position1.y is move.position2.y and move.position2.x is move.position1.x):
			print "ERROR, Bishop currently occupies that space, try a different move in is move blockable, you should not see this"
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
				
				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1
				#increment
				x =  x + m
				y = y + m	
			#print "bishop returned 1"
			return 0
				
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
				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1
				#increment
				x =  x + m
				y = y + (m * -1)
			#print "bishop returned 1"
			return 0
		else:
			print "isblockable this shouldnt happen ->Invalid Move: bishop move invalid!"
			return 0
		
	elif move.piece[1] == 'R':
		if (move.position1.x is move.position2.x):
			if (move.position2.y - move.position1.y) > 0:
				m = 1
			else:
				m = -1
			x = move.position1.x
			y = move.position1.y + m
			while (y*m) < (move.position2.y * m):
				if(x > 7 or x < 0 or y > 7 or y < 0):
					print "Invalid move: isblockable rook game logic error, you should not see this!"
					return 0
				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1

				y = y + m
			return 0
		elif move.position1.y is move.position2.y:
			if (move.position2.x - move.position1.x) > 0:
				m = 1
			else:
				m = -1
			y = move.position1.y
			x = move.position1.x + m
			while (x*m) < (move.position2.x * m):
				if(x > 7 or x < 0 or y > 7 or y < 0):
					print "Invalid move: isblockable game logic error, you should not see this!"
					return 0
				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1
				x = x + m
			return 0
		else:
			print "no block activated"
	 
	elif move.piece[1] == 'Q':
		if(move.position1.y is move.position2.y and move.position2.x is move.position1.x):
			print "ERROR, Queen currently occupies that space, try a different move in is move blockable, you should not see this"
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
					print "Invalid move: isvalid queen game logic error, you should not see this!"
					return 0
				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1

				#increment
				x =  x + m
				y = y + m	
			#print "bishop returned 1"
			return 0
				
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
					print "Invalid move: isvalid queen game logic error, you should not see this!"
					return 0
				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1
						#increment
				x =  x + m
				y = y + (m * -1)
			#print "bishop returned 1"
			return 0
		elif (move.position1.x is move.position2.x):
			if (move.position2.y - move.position1.y) > 0:
				m = 1
			else:
				m = -1
			x = move.position1.x
			y = move.position1.y + m
			while (y*m) < (move.position2.y * m):
				if(x > 7 or x < 0 or y > 7 or y < 0):
					print "Invalid move: isblockable rook game logic error, you should not see this!"
					return 0

				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1

				y = y + m
			return 0
		elif move.position1.y is move.position2.y:
			if (move.position2.x - move.position1.x) > 0:
				m = 1
			else:
				m = -1
			y = move.position1.y
			x = move.position1.x + m
			while (x*m) < (move.position2.x * m):
				if(x > 7 or x < 0 or y > 7 or y < 0):
					print "Invalid move: isblockable game logic error, you should not see this!"
					return 0

				isblocked, blockerpositions = isplacecovered(chessarray, gamestructure, blocker, makeposition(x, y), 1)
				if(isblocked is 1):
					for x1, bposition in enumerate(blockerpositions):
						if(ismoveintocheck(createmove(getpiecefrompos(chessarray, bposition), bposition, makeposition(x,y)), chessarray, gamestructure) is 0):
							print "that move is blockable!"
							print getpiecefrompos(chessarray, bposition)
							return 1

				x = x + m
		else:
			print "isblockable this shouldnt happen ->Invalid Move: bishop move invalid!"
			return 0

	elif move.piece[1] == 'K':
		return 0
	else:
		print "game logic error in moveplist, this shouldnt happen"
	return 0
		#get positions 1 and 2
		#figure out which quadrant it is in by checking using if statements
		#create start position
		#while position.x != position2.x and position.y != position2.y:
			#if iscoveredplace(position) 
				#return 1
		#return 0
		


#checks to see if a player can move to a certain position
#this is different than isvalid, because it checks if the move is into check
def canplayermovehere(chessarray, gamestructure, attackerplayer, positionin):
	canmovestatus, positions = isplacecovered(chessarray, gamestructure, attackerplayer, positionin, 1)
	if canmovestatus is 1:
		for x1, aposition in enumerate(positions):
			if ismoveintocheck(createmove(getpiecefrompos(chessarray, aposition), aposition, positionin), chessarray, gamestructure) is 0:
				return 1
	return 0

#this function checks for pawn promotion
def pawnpromotioncheck(move, chessarray, gamestructure):
	if move.piece[0] == 'W':
		mypieces = gamestructure.allpieces.white
	else:
		mypieces = gamestructure.allpieces.black

	if move.piece[1] == 'P' and (move.position2.y is 0 or move.position2.y is 7):
		print "PAWN PROMOTION!"
		
		removepieceplist(move.piece, move.position2, gamestructure)
		
		validinput = 0
		while validinput is 0:
			printboard(chessarray)
			input1 = raw_input("What piece would you like? Enter r for rook, q for queen, b for bishop, or k for knight  ")
			#print ("input1 is %s" %  (input1))
			inargs =  input1.split()
			#piece = inargs[0]
			#print len(inargs)
			if len(inargs) is 1:	
				if inargs[0] == '&':
					apiece = move.piece[0] + '&'
					mypieces.knights.append(move.position2)
					chessarray[move.position2.y][move.position2.x] = apiece[:]
					return
				elif inargs[0] == 'b':
					apiece = move.piece[0] + 'B'
					mypieces.bishops.append(move.position2)
					chessarray[move.position2.y][move.position2.x] = apiece[:]
					return
				elif inargs[0] == 'r':
					apiece = move.piece[0] + 'R'
					mypieces.rooks.append(move.position2)
					chessarray[move.position2.y][move.position2.x] = apiece[:]
					return
				elif inargs[0] == 'q':
					apiece = move.piece[0] + 'Q'
					mypieces.queens.append(move.position2)
					chessarray[move.position2.y][move.position2.x] = apiece[:]
					return
				else:
					print "incorrect usage: please enter one character r for rook, q for queen, b for bishop, or k for knight"

			
			else:
				print "incorrect usage: please enter one character r for rook, q for queen, b for bishop, or k for knight"


#ischeckmate
#
#this function is called after the current player has made a move to see if the other player is in check, checkmate, or stalemate.
#first the function checks to see if the other player is in check.  Then the function checks to see if the other player can move the king to any of 
#the surrounding positions. 

def ischeckmate(chessarray, gamestructure):
	#print "in ischeckmate"
	
	check = 0
	nomoveking = 0
	stalemate = 0

	checkresult, positions = isplacecovered(chessarray, gamestructure, gamestructure.currentplayer, gamestructure.otherplayer.pieces.king[0], 1)
		#if other player is in check...if current player covers location of 
	if checkresult is 1:
		gamestructure.otherplayer.checkflag = 1
		print "CHECK!"
		check = 1
		#print "position of check x axis is "
		#print positions[0].x

	#if king cannot move anywhere, and all other pieces cannot move anywhere
	#if isplace covered all positions surrounding king
	position1 = makeposition(gamestructure.otherplayer.pieces.king[0].x, gamestructure.otherplayer.pieces.king[0].y)
	aposition = [makeposition((position1.x-1), (position1.y+1)), makeposition(position1.x, position1.y+1), makeposition(position1.x+1, position1.y+1), makeposition(position1.x-1, position1.y-1), makeposition(position1.x, position1.y-1), makeposition(position1.x+1, position1.y-1), makeposition(position1.x-1, position1.y), makeposition(position1.x+1, position1.y)]

	#find out is king is trapped
	for i1 in range(0, 8):
		#print i1
		if(ispositioninbounds(aposition[i1])):
			if ((isplacecoveredfortake(chessarray, gamestructure, gamestructure.currentplayer, aposition[i1], 0) is 0) and (issamecolor(gamestructure.otherplayer,getpiecefrompos(chessarray, aposition[i1])) is 0)):
				#print "hole is"
				#print i1
				#print "place covered is"
				#print isplacecoveredfortake(chessarray, gamestructure, gamestructure.currentplayer, aposition[i1], 0)
				#print "is same color is"
				#print issamecolor(gamestructure.otherplayer,getpiecefrompos(chessarray, aposition[i1]))
				#return 0
				return 0 
		#print "position covered is"
		#print i1
	
	#print "testing message: King is trapped!"
	#return 0	
	#if king is in check (and obviously trapped, otherwise function would have returned)
	if check is 1:
		#check for checkmate
		#you could see if the king is in double check or not
		#iterate through all current pieces, if that piece is attacking the king, keep track of it.  

		#if double check
		print "check happened"
		print "length positions is"
		print len(positions)
		if len(positions) > 1: #if there is more than one piece attacking the king
			print "CHECKMATE!"
			return 1 #this is returned to exitflag, should end the game
		elif len(positions) is 1:
			print "one piece placing check, and king trapped.  doing checkmate check"
			#make position1 position of attacking piece
			#makeposition 2 position of king
			#make piece getpiecefrompos(position1)
			apiece = getpiecefrompos(chessarray, positions[0])
			aposition1 = positions[0]
			aposition2 = gamestructure.otherplayer.pieces.king[0]
			#print "position 1 x y is"
			#print aposition1.x
			#print aposition1.y
		
			#print "position2 xy is"
			#print aposition2.x
			#print aposition2.y
		
			move1 = createmove(apiece, aposition1, aposition2)
			#print getpiecefrompos(chessarray, positions[0])
				
			#make move
			if ismoveblockable(move1, chessarray, gamestructure, gamestructure.currentplayer, gamestructure.otherplayer) or canplayermovehere(chessarray, gamestructure, gamestructure.otherplayer, aposition1):
				print "No Checkmate.  Check can be disrupted."
			else: 
				print "Checkmate!"
				return 1
						
		else:  
			#if player cannot block the attack, or take the piece
			print "game logic error in ischeckmate, this should not happen"
				#print "CHECKMATE!"

	else:	#(king is not in check but is trapped)
		#check for stalemate
			
		#stalemate is not possible with queens
		if (len(gamestructure.otherplayer.pieces.queens) is 0):
			print "NO QUEEN, STARTING STALEMATE CHECK"
			#for all positions
				#for all pieces
					#if apiece can make a legal move that is not into check, then there is no stalemate
			blockPrint()
			for j in range(0, 8):
				for k in range(0, 8):
					position2 = makeposition(j, k)
					if issamecolor(gamestructure.otherplayer, getpiecefrompos(chessarray, position2)) is 0:
						for position1 in gamestructure.otherplayer.pieces.pawns:
							blockPrint()
							newmove = createmove(getpiecefrompos(chessarray, position1), position1, position2)
							if isvalidpawn(newmove, chessarray, gamestructure) and (ismoveintocheck(newmove, chessarray, gamestructure) is 0):
								enablePrint()
								printPosition(position1, chessarray)
								return 0
						for position1 in gamestructure.otherplayer.pieces.knights:
							blockPrint()
							newmove = createmove(getpiecefrompos(chessarray, position1), position1, position2)
							if isvalidknight(newmove, chessarray, gamestructure) and (ismoveintocheck(newmove, chessarray, gamestructure) is 0):
								enablePrint()
								printPosition(position1, chessarray)
								return 0
						for position1 in gamestructure.otherplayer.pieces.bishops:
							blockPrint()
							newmove = createmove(getpiecefrompos(chessarray, position1), position1, position2)
							if isvalidbishop(newmove, chessarray, gamestructure) and (ismoveintocheck(newmove, chessarray, gamestructure) is 0):
								enablePrint()
								printPosition(position1, chessarray)
								return 0
						for position1 in gamestructure.otherplayer.pieces.rooks:
							blockPrint()
							newmove = createmove(getpiecefrompos(chessarray, position1), position1, position2)
							if isvalidrook(newmove, chessarray, gamestructure) and (ismoveintocheck(newmove, chessarray, gamestructure) is 0):
								enablePrint()
								printPosition(position1, chessarray)
								return 0
						for position1 in gamestructure.otherplayer.pieces.king:
							blockPrint()
							newmove = createmove(getpiecefrompos(chessarray, position1), position1, position2)
							if isvalidking(newmove, chessarray, gamestructure):
								if(ismoveintocheck(newmove, chessarray, gamestructure) is 0):
									enablePrint()
									printPosition(position1, chessarray)
									return 0
			enablePrint()
			print "STALEMATE!"
			return 1
	return 0

#makegamestructure
#
#this function takes command line input to establish whether each player will be human or computer
#and if playerone will be playing as white, black, or will be randomly assigned
def makegamestructure():
	print "Welcome to the command line chess game!"
	gameinitiated = 0
	#gamestructure = Gamestructure()	
	while gameinitiated is 0:
		
		print "Will player one be playing as a human or computer today? "
		input1 = raw_input("Enter h for human or c for computer ")
		if(input1 == "h" or input1 == "H"):  
			p1type = 0	
		elif input1 == "c" or input1 == "C":
			print "Computer play is currently disabled.  Program will default to human."
			p1type = 0
		else:
			print "Invalid Input! lets try this again."
			continue

		print "Will player two be playing as a human or computer today? "
		input1 = raw_input("Enter h for human or c for computer ")
		if(input1 == "h" or input1 == "H"):  
			p2type = 0	
		elif input1 == "c" or input1 == "C":
			print "Computer play is currently disabled.  Program will default to human."
			p2type = 0
		else:
			print "Invalid Input! lets try this again."
			continue

		print "Will player one be white, black or random today"
		input1 = raw_input("Enter w for white, b for black, or r for random ")
		if(input1 == "w" or input1 == "W"):  
			status = 1
			
		elif input1 == "b" or input1 == "B":
			status  = 2
		elif input1 == "R" or input1 == "r":
			pstat = random.randrange(1,2)	
			if pstat is 1:
				status = 1
				#amestructure.playerone.color = "W"
				#amestructure.playertwo.color = "B"
				#amestructure.currentplayer = gamestructure.playerone
				#amestructure.otherplayer = gamestructure.playertwo
				#amestructure.playerone.pieces = gamestructure.allpieces.white
				#amestructure.playertwo.pieces = gamestructure.allpieces.black

				#amestructure.current = 1

			else:
				status = 2
				#amestructure.playerone.color = "B"
				#amestructure.playertwo.color = "W"
				#amestructure.currentplayer = gamestructure.playertwo
				#amestructure.otherplayer = gamestructure.playerone
				#amestructure.playertwo.pieces = gamestructure.allpieces.white
				#amestructure.playerone.pieces = gamestructure.allpieces.black

				#amestructure.current = 2

		else:
			print "Invalid Input! lets try this again."
			continue
		gameinitiated = 1	
		return makeGamestructure(status, p1type, p2type)

#change game structure to next turn
def nextturn(gamestructure):
	#reset player flags
	gamestructure.currentplayer.castleflag = 0
	gamestructure.currentplayer.pawnpflag = 0
	
	for places in gamestructure.currentplayer.enpassantvalid:
		del gamestructure.currentplayer.enpassantvalid[0]
	if len(gamestructure.currentplayer.enpassantvalid) != 0:
		print "Error en passant array not emptied"
		gamestructure.currentplayer.enpassantvalid = []

	gamestructure.currentplayer.checkflag = 0
	
	if(gamestructure.current is 1 and gamestructure.currentplayer is gamestructure.playerone):
		gamestructure.current = 2
		gamestructure.currentplayer = gamestructure.playertwo
		gamestructure.otherplayer = gamestructure.playerone
	elif(gamestructure.current is 2 and gamestructure.currentplayer is gamestructure.playertwo):
		gamestructure.current = 1
		gamestructure.currentplayer = gamestructure.playerone
		gamestructure.otherplayer = gamestructure.playertwo
	else:
		for i in range(10):
			print "ERROR with next turn this should not happen game logic error"
	return

#initializes the chess array data structure
def initchessarray():
	chessarr = [["WR", "W&", "WB", "WK", "WQ", "WB", "W&", "WR"],['WP','WP','WP','WP','WP','WP','WP','WP'],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["BP","BP","BP","BP","BP","BP","BP","BP"],["BR", "B&", "BB", "BK", "BQ", "BB", "B&", "BR"]]
	return chessarr
	
