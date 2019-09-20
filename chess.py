import numpy as np 
import sys


straightGrad = (0)
diagGrad = (1,-1)

def getIntercept(y,x):
    return y - lookup((y,x))*x

def checkIntercept(yStart, xStart, yEnd, xEnd):
    return lookup((yStart,xStart))*xEnd+getIntercept(yStart,xStart) == yEnd



class game():
	def __init__(self):
                self.Mate = False
                self.board = self.setupBoard()
                self.playerColour = input("Whites or blacks? ") 
                self.peices = [[' ♖ ',' ♘ ',' ♗ ',' ♕ ',' ♔ ',' ♙ '],[' ♜ ',' ♞ ',' ♝ ',' ♛ ',' ♚ ',' ♟ ']]
			
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


		#some hard code to make the board look nice
		board[-1][[0,1,-1]] = ' '
		board[0][1] = ''
		board[0][0] = '|'
		board[-1][0] = ' '
		board[-2][0] = ' '
		board[-2][-2] = ' = '

		return board

	def show(self):
		print('\n',''.join(np.insert(self.board, [i*11 for i in range(1,12)], '\n')), '\n')

	def getColour(self,y,x):
		return 'black' if ord((self.board[y][x])[1:2]) <= 9817 else 'white'

	def search(self, yStart, xStart, colour, direction, yEnd, xEnd): 
		targets = self.peices[[0 if colour == 'white' else 1][0]]
		if direction == 'diagonal':
			incrementList = [(1,1),(1,-1),(-1,1),(-1,-1)]
		if direction == 'linear':
			incrementList = [(-1,0),(0,-1),(1,0),(0,1)]

		for yInc,xInc in incrementList: #Allows us to transverse in one direction incrementally at a time.
			peiceFound = False
			while not peiceFound: 
				y,x = (yStart+yInc,xStart+xInc)
				position = self.board[y][x]
				if position in (' = ', '|') or position in self.peices[0] or position in self.peices[1]: #check if direction has found any other peice or board edge
					if (y,x) == (yEnd,xEnd) and position in targets:
						return True	
					peiceFound = True
				elif (y,x) == (yEnd,xEnd):
					return True	#works for taking too as function goes upto and including first peice

				if xInc > 0:  #Keeps 0's at 0 and -1 deincrementing
					xInc+=1
				if yInc > 0:
					yInc+=1
				if xInc < 0:
					xInc-=1
				if yInc < 0: 
					yInc-=1

		return False

	def pawnSearch(self, yStart, xStart, colour, yEnd, xEnd): #TODO: implement french thing
		targets = self.peices[[0 if colour == 'white' else 1][0]]
		limit = 1
		c = 0
		peiceFound = False
		if colour == 'white':
			if yStart == 7:
				limit <<= 1
			increment = (-1,0)
			take = [(-1,-1),(-1,1)]
			upgradeRow = 1
		if colour == 'black':
			if yStart == 2:
				limit <<= 1
			increment = (1,0)
			take = [(1,-1),(1,1)]
			upgradeRow = 8
		yInc = increment[0]
		xInc = increment[1]
		
		if self.board[yEnd][xEnd] in targets:
			for coords in take:
				yInc = coords[0]
				xInc = coords[1]
				y,x = (yStart+yInc, xStart+xInc)
				
				if (y,x) == (yEnd,xEnd):
					if yEnd == upgradeRow:
						self.pawnUpgrade(colour, yStart, xStart)
					return True
			return False
		else:
			while not peiceFound and c != limit:
				y,x = (yStart+yInc, xStart+xInc)
				position = self.board[y][x]
				if position in (' = ', '|') or position in self.peices[0] or position in self.peices[1]:
					return False
				elif (y,x) == (yEnd,xEnd):
					if yEnd == upgradeRow:
						self.pawnUpgrade(colour, yStart, xStart)
					return True

				if yInc > 0:
					yInc+=1
				if yInc < 0:
					yInc-=1
				c+=1

	def pawnUpgrade(self, colour, y, x):
		selection = [i for i in self.peices[[0 if colour == 'black' else 1][0]] if i not in (' ♟ ',' ♚ ', ' ♔ ', ' ♙ ')] #filter peices that can't be upgraded to
		names = ["rook", "knight", "bishop", "queen"]
		peiceDict = {name:i for name, i in zip(names,selection)}
		upgradeTo = input("Enter peice to upgrade to (Queen, Knight, Bishop, Rook): ").lower()
		self.board[y][x] = peiceDict[upgradeTo] #this gets overridden by the move function


	def knightSearch(self, yStart, xStart, colour, yEnd, xEnd):
		targets = self.peices[[0 if colour == 'white' else 1][0]]
		increment = [(-2,1),(-1,2),(-2,-1),(-1,-2),(2,1),(2,-1),(1,-2),(1,2)]
		for i in increment:
			y,x = (yStart+i[0], xStart+i[1])
			position = self.board[y][x]
			if position in (' - ', ' x ') or position in targets:
				if (y,x) == (yEnd,xEnd):
					return True

	def kingSearch(self, yStart, xStart, colour, yEnd, xEnd):
		increments = [(1,1),(-1,-1),(1,-1),(-1,1),(0,1),(1,0),(-1,0),(0,-1)]
		allyes = self.peices[[0 if colour == 'black' else 1][0]]
		for yInc,xInc in increments:
			y,x = (yStart+yInc,xStart+xInc)
			position = self.board[y][x]
			if position not in ('|', ' = ') and position not in allyes:
				if (y,x) == (yEnd,xEnd):
					return True
		return False

	#TODO: make more efficeint by only calculating peices in king's line of sight, not all peices
	def inCheck(self, colour):
		targets = self.peices[[0 if colour == 'white' else 1][0]]
		breaking = False
		king = [' ♚ ' if colour == 'white' else ' ♔ '][0]

		for y in range(1,9): #start by finding the king
			for x in range(2,10):
				if self.board[y][x] == king:
					self.kingPos = (y,x)
					breaking = True
					break
			if breaking == True: #god I wish python let you break out of nested loops easier
				break

		for y in range(1,9):
			for x in range(2,10):
				if self.board[y][x] in targets:
					if self.ruleCheck(y, x, self.kingPos[0], self.kingPos[1]) == True: 
						return True

		return False

	def ruleCheck(self, yStart, xStart, yEnd, xEnd): 
		colour = self.getColour(yStart,xStart)
		peice = self.board[yStart][xStart]

		if peice in (' ♖ ', ' ♜ ') :
			return self.search(yStart, xStart, colour, 'linear', yEnd, xEnd)
		if peice in (' ♗ ', ' ♝ '):
			return self.search(yStart, xStart, colour, 'diagonal', yEnd, xEnd)
		if peice in (' ♕ ', ' ♛ '):
			return (self.search(yStart, xStart, colour, 'diagonal', yEnd, xEnd) or self.search(yStart, xStart, colour, 'linear', yEnd, xEnd))
		if peice in (' ♞ ', ' ♘ '):
			return self.knightSearch(yStart, xStart, colour, yEnd, xEnd)
		if peice in (' ♟ ', ' ♙ '):
			return self.pawnSearch(yStart, xStart, colour, yEnd, xEnd)
		if peice in (' ♚ ', ' ♔ '):
			return self.kingSearch(yStart, xStart, colour, yEnd, xEnd)

	def move(self): 
		while True:
			malformed = False
			move = input('Enter move: ')

			if move == 'exit':
				sys.exit()

			try:
				start, end = move.split(' ') 
			except ValueError:
				print('Illegal move')
				malformed = True
				
			if not malformed:
				for xChar, yChar in [start,end]:
					if not xChar.isalpha() or not yChar.isdigit():
						print('Illegal move')
						malformed = True
					elif ord(xChar) < ord('a') or ord(xChar) > ord('h'):
						print('Illegal move')
						malformed = True

			if not malformed:
				yStart = 9-int(start[1]) #9 minus value as chess is decending while the matrix is increasing
				xStart = (ord(start[0]) - 97)+2 #a's ascii code is 97 (+2 for indexing)
				yEnd = 9-int(end[1])
				xEnd = (ord(end[0]) - 97)+2

				colour = self.getColour(yStart, xStart)

				if self.ruleCheck(yStart, xStart, yEnd, xEnd):
					target = self.board[yEnd][xEnd] #saves whatever was in square in case move is still illegal
					self.board[yEnd][xEnd] = self.board[yStart][xStart]
					self.board[yStart][xStart] = [' - ' if (xStart+yStart+1)%2 == 0 else ' x '][0]
					if self.inCheck(colour):
						self.board[yStart][xStart] = self.board[yEnd][xEnd]
						self.board[yEnd][xEnd] = target
						print("Move sustains/places you in check.")
					else:
						break
				else:
					print("Illegal move")


if __name__ == '__main__':
	game = game()
	while not game.Mate:
		game.show()
		game.move()
