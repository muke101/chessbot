import numpy as np 
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

checkMate = False

print(''.join(np.insert(board, [i*10 for i in range(1,10)], '\n')), '\n')
move = input('Enter move: ')
start, end = move.split(' ')
yStart = int(start[1])-1
xStart = ord(start[0]) - 97 #a's ascii code is 97
yEnd = int(end[1])-1
xEnd = ord(end[0]) - 97
board[yEnd][xEnd] = board[yStart][xStart]
print(board[yStart][xStart])
board[yStart][xStart] = [' - ' if (xStart+yStart+1)%2 == 0 else ' x '][0]
print([' - ' if (xStart+yStart+1)%2 == 0 else ' x '][0])
print(''.join(np.insert(board, [i*10 for i in range(1,10)], '\n')), '\n')

