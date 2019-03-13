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
		board = np.empty((12,10), dtype=object) #empty over zeros for that s p e e d
		board[0, [i for i in range(9)]] = ' = '
		board[11, [i for i in range(9)]] =  ' = '
		board[0][-1] = ' '
		board[11][-1] = ' '
		for y in range(1,11): 
			for x in range(10): 
				if x == 0 or x == 9:
					board[y][x] = '|'
				else:
					board[y][x] = [' - ' if (x+y+1)%2 == 0 else ' x '][0] #- is white space, x is black
		
		peices = [[' ♖ ',' ♘ ',' ♗ ',' ♕ ',' ♔ ',' ♗ ',' ♘ ',' ♖ '],[' ♜ ',' ♞ ',' ♝ ',' ♛ ',' ♚ ',' ♝ ',' ♞ ',' ♜ ']]
		for c,y in enumerate([1,-2]):
			for x in range(1,9):
				board[y][x] = peices[c][x-1]
				
		board[2][[i for i in range(1,9)]] = ' ♙ '
		board[-3][[i for i in range(1,9)]] = ' ♟ '

		return board

	def show(self):
		print(''.join(np.insert(self.board, [i*10 for i in range(1,12)], '\n')), '\n')

	def neighborSearch(self, y, x, increment, colour, direction): #this is either cursed or genius
		peiceFound = False
		targets = self.peices[[0 if colour == 'white' else 1][0]]
		if direction == 'diagonal':
			neighbors = [(x+increment,y+increment),(x-increment,y+increment),(x+increment,y-increment),(x-increment,y-increment)]
		if direction == 'linear':
			neighbors = [(x+increment,y),(x,y+increment),(x-increment,y),(x,y-increment)] #TODO: check these line up
		for i in range(4):
			while not peiceFound:
				result = filter(lambda lookup: self.board[y][x] in (' - ', ' x ', targets), neighbors[i])
				if self.board[y][x] in targets: #TODO: this is wrong
					peiceFound == True
				for i in result: #TODO: something fucky is happening here
					print(i)
				if len(list(result)) != 0:
					yield result
				else:
					yield 0

	def ruleCheck(self, yStart, xStart, yEnd, xEnd):
		c = 0
		#use colour codes to determine peice colour
		#determine what peice and how it can move and it's limit, call functions appropiately
		limit = 1
		i = 0
		breaking = False
		while c != limit: 
			for j in self.neighborSearch(yStart,xStart, i, 'white', 'linear'):
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
			move = input('Enter move: ')
			start, end = move.split(' ')

			yStart = 9-(int(start[1])-1) #9 minus value as chess is decending while the matrix is increasing, minus 1 as chess isn't 0 indexed
			xStart = (ord(start[0]) - 97)+1 #a's ascii code is 97(+1 for indexing)
			yEnd = 9-(int(end[1])-1)
			xEnd = (ord(end[0]) - 97)+1

			if self.ruleCheck(yStart, xStart, yEnd, xEnd):
				self.board[yEnd][xEnd] = self.board[yStart][xStart]
				self.board[yStart][xStart] = [' - ' if (xStart+yStart+1)%2 == 0 else ' x '][0]
				break
			else:
				print("illegal move")


game()
