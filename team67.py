MAX_VAL = 2**63

def checkX(mask, pos):
	return (mask & (1 << (pos + pos))) != 0

def checkO(mask, pos):
	return (mask & (1 << (pos + pos + 1))) != 0

def flipboard(mask):
	for i in xrange(16):
		if checkX(mask, i) or checkO(mask, i):
			mask ^= ( (1 << (pos + pos)) + (1 << (pos + pos + 1)) )
	return mask

def match_win(mask):
	# Rows and columns
	if checkX(mask, 0) and checkX(mask, 0 + 1) and checkX(mask, 0 + 2) and checkX(mask, 0 + 3):
		return True
	if checkX(mask, 0) and checkX(mask, 0 + 4) and checkX(mask, 0 + 8) and checkX(mask, 0 + 12):
		return True

	if checkX(mask, 4) and checkX(mask, 4 + 1) and checkX(mask, 4 + 2) and checkX(mask, 4 + 3):
		return True
	if checkX(mask, 1) and checkX(mask, 1 + 4) and checkX(mask, 1 + 8) and checkX(mask, 1 + 12):
		return True

	if checkX(mask, 8) and checkX(mask, 8 + 1) and checkX(mask, 8 + 2) and checkX(mask, 8 + 3):
		return True
	if checkX(mask, 2) and checkX(mask, 2 + 4) and checkX(mask, 2 + 8) and checkX(mask, 2 + 12):
		return True

	if checkX(mask, 12) and checkX(mask, 12 + 1) and checkX(mask, 12 + 2) and checkX(mask, 12 + 3):
		return True
	if checkX(mask, 3) and checkX(mask, 3 + 4) and checkX(mask, 3 + 8) and checkX(mask, 3 + 12):
		return True
	# Diamonds
	if checkX(mask, 1) and checkX(mask, 1 + 3) and checkX(mask, 1 + 5) and checkX(mask, 1 + 8):
		return True
	if checkX(mask, 2) and checkX(mask, 2 + 3) and checkX(mask, 2 + 5) and checkX(mask, 2 + 8):
		return True
	if checkX(mask, 5) and checkX(mask, 5 + 3) and checkX(mask, 5 + 5) and checkX(mask, 5 + 8):
		return True
	if checkX(mask, 6) and checkX(mask, 6 + 3) and checkX(mask, 6 + 5) and checkX(mask, 6 + 8):
		return True
	return False

def match_loss(mask):
	return match_win(flipboard(mask))


class Team67():

	def __init__(self):
		self.last_win = False
		self.level = 0
		self.cached_states = []
		self.zobrist_hash = 0
		self.zobrist_values = [[], []]
		for i in xrange(256):
			self.zobrist_values[0].append(random.randint(0, MAX_VAL))
			self.zobrist_values[1].append(random.randint(0, MAX_VAL))
		self.board = [0 for i in xrange(16)]

		# 0 : No winner rn, 1 : X, 2 : O
		self.block_winner = [0 for i in xrange(16)] 

	def checkX(mask, pos):
		return (mask & (1 << (pos + pos))) != 0

	def checkO(mask, pos):
		return (mask & (1 << (pos + pos + 1))) != 0

	def getValidMoves(old_move):

		valid_moves = []
		block_x, block_y = old_move[0] >> 2, old_move[1] >> 2
		block = (block_x << 2) + block_y

		possible = False
		if self.block_winner[block] == 0:
			for position in xrange(16):
				if self.checkX(self.board[block], position) or self.checkO(self.board[block], position):
					pass
				else:
					possible = True
					valid_moves.append((position / 4), position & 3)

		if possible:
			return valid_moves

		for block in xrange(16):
			if self.block_winner[block] != 0:
				continue
			for position in xrange(16):
				if self.checkX(self.board[block], position) or self.checkO(self.board[block], position):
					pass
				else:
					valid_moves.append((position / 4), position & 3)
		return valid_moves				

	def minimax(depth, alpha, beta, isMaximizing, old_move, current_hash, bonus_used):
		# check terminal state here

		if (current_hash, isMaximizing, bonus_used) in self.cached_states:
			return self.cached_states[(current_hash, isMaximizing, bonus_used)]

		valid_moves = getValidMoves(old_move)

		new_val = 0
		if isMaximizing:
			new_val = -MAX_VAL
			for current_move in valid_moves:

				# update changes in global variables here
				win_block, updated_hash = update()
				
				if win_block and not bonus_used:
					t_val = self.minimax(depth - 1, alpha, beta, isMaximizing, current_move, updated_hash, True)
				else:
					t_val = self.minimax(depth - 1, alpha, beta, not isMaximizing, current_move, updated_hash, False)

				if t_val > new_val:
					if self.level == depth:
						self.best_move = current_move
					new_val = t_val

				if alpha < new_val:
					alpha = new_val

				# revert changes in global variables here

				if beta <= alpha:
					break
		
		else:
			pass

		self.cached_states[(current_hash, isMaximizing, bonus_used)] = new_val
		return new_val


	def move(self, board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"
			
		self.zobrist_hash ^= self.zobrist_values[1][old_move[0] * 16 + old_move[1]]
		block_x, block_y = old_move[0] >> 2, old_move[1] >> 2
		block = (block_x << 2) + block_y
		pos_x, pos_y = old_move[0] & 3, old_move[1] & 3 
		self.board[block] |= (1 << (1 + ((pos_y + (pos_x << 2)) << 1)))
		
		if match_loss(self.board[block]):
			self.block_winner[block] = 2

		current_move = (-1, -1)
		for depth in xrange(255):
			self.cached_states = []
			self.level = depth
			self.minimax(depth, ALPHA, BETA, 1, old_move, self.zobrist_hash, self.last_win)
			current_move = self.best_move

		old_move = current_move
		self.zobrist_hash ^= self.zobrist_values[0][old_move[0] * 16 + old_move[1]]
		block_x, block_y = old_move[0] >> 2, old_move[1] >> 2
		block = (block_x << 2) + block_y
		pos_x, pos_y = old_move[0] & 3, old_move[1] & 3 
		self.board[block] |= (1 << (((pos_y + (pos_x << 2)) << 1)))
		
		if match_win(self.board[block]):
			self.block_winner[block] = 1
			self.last_win = True

		else:
			self.last_win = False

		return current_move
		# mvp = raw_input()
		# mvp = mvp.split()
		# return (int(mvp[0]), int(mvp[1]))

