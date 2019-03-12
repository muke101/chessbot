import numpy as np 

class game():
	def __init__(self):
		self.checkMate = False
		self.board = self.setupBoard()
		self.show()
		self.move()
		self.show()

	def setupBoard(self):
		board = np.empty((10,10), dtype=object) #empty over zeros for that s p e e d
		for y in range(10): 
			for x in range(10): 
				if x == 0 or x == 9:
					board[y][x] = '|'
				else:
					board[y][x] = [' - ' if (x+y+1)%2 == 0 else ' x '][0] #- is white space, x is black
		peices = [[' ♖ ',' ♘ ',' ♗ ',' ♕ ',' ♔ ',' ♗ ',' ♘ ',' ♖ '],[' ♜ ',' ♞ ',' ♝ ',' ♛ ',' ♚ ',' ♝ ',' ♞ ',' ♜ ']]
		for y in [0,-1]:
			for x in range(1,9):
				board[y][x] = peices[y][x-1]
		board[1][[i for i in range(1,9)]] = ' ♙ '
		board[-2][[i for i in range(1,9)]] = ' ♟ '
		return board

	def show(self):
		print(''.join(np.insert(self.board, [i*10 for i in range(1,10)], '\n')), '\n')

	def move(self):
		move = input('Enter move: ')
		start, end = move.split(' ')

		yStart = 9-(int(start[1])-1) #9 minus position as chess is decending while the matrix is increasing
		xStart = ord(start[0]) - 96 #a's ascii code is 97(+1 for indexing)
		yEnd = 9-(int(end[1])-1) #minus 1 as chess isn't 0 indexed
		xEnd = ord(end[0]) - 96

		self.board[yEnd][xEnd] = self.board[yStart][xStart]
		self.board[yStart][xStart] = [' - ' if (xStart+yStart+1)%2 == 0 else ' x '][0]


game()
