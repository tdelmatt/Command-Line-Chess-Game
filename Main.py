#############################################################
##Name: Taylor Del Matto
##Course: CS 419
##Final Project: Chess Game
##Main
##Description: This is where we invoke primary functions in the game loop, and run the actual game.  
#############################################################
import random
import copy
import sys, os
import pdb
from gamestructure import *
from  builder_functions import *
from primary_functions import *


#GAME PLAY STARTS HERE

#init chessarray
chesslist = initchessarray()

#initialize gamestructure from command line input
gamestr = makegamestructure()

#initialize variables
exitflag = 0
move2 = Move()

#printboard(chesslist)
#GAME LOOP
#game ends when exit is entered, or game end is reached
while exitflag is 0:	
	move2.valid = 0
	#get move/validate move cycle ends when valid move is entered
	while move2.valid is 0 and exitflag != 1:
		
		#these copy the gamestate to pass to the AI, so that
		#the original game state is not corrupted
		gamestate2 = copygamestate(gamestr)
		chessarray2 = copy.deepcopy(chesslist)

		#get move from user
		move2, exitflag = getmove(gamestr, chesslist, exitflag)
		
		#if no exit flag check validity of move
		if exitflag is 0:
			isvalid(move2, chesslist, gamestr)
	
	#if there is an exit flag, skip to next iteration of loop, where game will be ended
	if exitflag is 1:
		continue
	
	#move piece in piece list
	moveplist(move2, gamestr)
	
	#move piece in chess array
	movepiece(gamestr, chesslist, move2)
	
	#check for pawn promotion
	pawnpromotioncheck(move2, chesslist, gamestr)
	
	#check for checkmate
	exitflag = ischeckmate(chesslist, gamestr)
	
	#initialize next turn
	nextturn(gamestr)

