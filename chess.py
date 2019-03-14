import numpy as np 
import collections

class game():
	def __init__(self):
		self.checkMate = False
		self.board = self.setupBoard()
		self.peices = [[' ♖ ',' ♘ ',' ♗ ',' ♕ ',' ♔ ',' ♙ '],[' ♜ ',' ♞ ',' ♝ ',' ♛ ',' ♚ ',' ♟ ']]
		self.show()
		self.move()
		self.show()

	def setupBoard(self):
		board = np.empty((11,11), dtype=object) #empty over zeros for that s p e e d
		board[0, [i for i in range(2,10)]] = ' = '
		board[9, [i for i in range(9)]] =  ' = '
		board[0][-1] = '| '
		board[9][-1] = '  '
		for c, y in enumerate(range(1,11)): 
			for j, x in enumerate(range(11)): 
				if x == 0:
					board[y][x] = str(8-c)
				elif (x== 1 or x == 10) and y < 10:
					board[y][x] = '|'
				elif y == 10 and x < 10:
					board[y][x] = ' '+chr(97+j-2)+' '
				elif y < 9:
					board[y][x] = [' - ' if (x+y+1)%2 == 0 else ' x '][0] #- is white space, x is black

		#arranging peice list in order it's layed out just for this loop
		peices = [[' ♖ ',' ♘ ',' ♗ ',' ♕ ',' ♔ ',' ♗ ',' ♘ ',' ♖ '],[' ♜ ',' ♞ ',' ♝ ',' ♛ ',' ♚ ',' ♝ ',' ♞ ',' ♜ ']]
		for c,y in enumerate([1,-3]):
			for x in range(2,10):
				board[y][x] = peices[c][x-2]
				
		board[2][[i for i in range(2,10)]] = ' ♙ '
		board[-4][[i for i in range(2,10)]] = ' ♟ '


		#some hard codes to make the board look nice
		board[-1][[0,1,-1]] = ' '
		board[0][1] = ''
		board[0][0] = '|'
		board[-1][0] = ' '
		board[-2][0] = ' '
		board[-2][-2] = ' = '

		return board

	def show(self):
		print('\n',''.join(np.insert(self.board, [i*11 for i in range(1,12)], '\n')), '\n')

	def neighborSearch(self, yStart, xStart, yEnd, xEnd, increment, colour, direction): #this is either cursed or genius
		targets = self.peices[[0 if colour == 'white' else 1][0]]
		if direction == 'diagonal':
			incrementList = [(1,1),(1,-1),(-1,1),(-1,-1)]
		if direction == 'linear':
			incrementList = [(1,0),(0,1),(-1,0),(0,-1)]

		for yInc,xInc in incrementList: #Allows us to transverse in one direction incrementally at a time.
			peiceFound = False
			while not peiceFound:
				y,x = (yStart+yInc,xStart+xInc)

				if self.board[y][x] in (' = ', ' | ', self.peices): #check if direction has found any other peice or board edge
					peiceFound = True #indicate this direction is a dead end
				if (y,x) == (yEnd,xEnd): #destination found with legal means
					return True	#works for taking too as function goes upto and including first peice

				if xInc > 0:  #Keeps 0's at 0 and -1 deincrementing
					xInc+=1
				if yInc > 0:
					yInc+=1
				if xInc < 0:
					xInc-=1
				if yInc < 0: #is this horribly hacky I wonder? Hope not.
					yInc-=1

		return False #all directions exhausted without destination found

	def ruleCheck(self, yStart, xStart, yEnd, xEnd):
		c = 0
		#use colour codes to determine peice colour
		#determine what peice and how it can move and it's limit, call functions appropiately
		limit = 1
		i = 0
		breaking = False
		while c != limit: 
			gen = self.neighborSearch(yStart,xStart, i, 'white', 'linear') #generator not reevaulated each iteration, i=0 for whole for loop
			for j in gen:
				if j == 0:
					breaking = True
					break
				for y,x in j:
					if (y,x) == (yEnd, xEnd):
						return True
				i+=1
			if breaking == True:
				break
			c+=1
		return False



	def move(self): 
		while True:
			move = input('Enter move: ') #TODO: make sure input in constrained to grid (a-h, 1-8)
			start, end = move.split(' ')

			yStart = 9-(int(start[1])) #9 minus value as chess is decending while the matrix is increasing
			xStart = (ord(start[0]) - 97)+2 #a's ascii code is 97 (+2 for indexing)
			yEnd = 9-(int(end[1]))
			xEnd = (ord(end[0]) - 97)+2
			if self.ruleCheck(yStart, xStart, yEnd, xEnd):
				self.board[yEnd][xEnd] = self.board[yStart][xStart]
				self.board[yStart][xStart] = [' - ' if (xStart+yStart+1)%2 == 0 else ' x '][0]
				break
			else:
				print("illegal move")


game()
