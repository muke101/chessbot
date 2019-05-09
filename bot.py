import chess

class bot(chess.game):
	def __init__(self):
		self.board = self.setupBoard()
		self.show()

bot()