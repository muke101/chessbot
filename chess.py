import numpy as np 
m = np.empty((10,10), dtype=object) #empty over zeros for that s p e e d

for c, y in enumerate(range(10)): 
	for x in range(10): 
		if x == 0 or x == 9:
			m[y][x] = '|'
		else:
			m[y][x] = [' - ' if (x+c)%2 == 0 else ' x '][0] #- is white space, x is black

peices = [[' ♖ ',' ♘ ',' ♗ ',' ♕ ',' ♔ ',' ♗ ',' ♘ ',' ♖ '],[' ♜ ',' ♞ ',' ♝ ',' ♛ ',' ♚ ',' ♝ ',' ♞ ',' ♜ ']]

for y in [0,-1]:
	for x in range(1,9):
		m[y][x] = peices[y][x-1]

m[1][[i for i in range(1,9)]] = ' ♙ '
m[-2][[i for i in range(1,9)]] = ' ♟ '

print(''.join(np.insert(m, [i*10 for i in range(1,10)], '\n')), '\n')

