from random import randint
import time
import signal

MAX_VAL = 2**63

def checkX(mask, pos):
	return (mask & (1 << (pos + pos))) != 0

def checkO(mask, pos):
	return (mask & (1 << (pos + pos + 1))) != 0

def flipboard(mask):
	for i in xrange(16):
		if checkX(mask, i) or checkO(mask, i):
			mask ^= ( (1 << (i + i)) + (1 << (i + i + 1)) )
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
		self.cached_states = {}
		self.zobrist_hash = 0
		self.zobrist_values = [[], []]
		for i in xrange(256):
			self.zobrist_values[0].append(randint(0, MAX_VAL))
			self.zobrist_values[1].append(randint(0, MAX_VAL))
		self.board = [0 for i in xrange(16)]

		# 0 : No winner rn, 1 : X, 2 : O
		self.block_winner = [0 for i in xrange(16)] 

	def signal_handler(self, signum, frame):
		raise Exception('Timed out!')

	def checkX(self, mask, pos):
		return (mask & (1 << (pos + pos))) != 0

	def checkO(self, mask, pos):
		return (mask & (1 << (pos + pos + 1))) != 0

	def getValidMoves(self, old_move):

		valid_moves = []
		(move_bx, move_by) = (old_move[0] & 3, old_move[1] & 3) 
		move_b = (move_bx << 2) + move_by
		possible = False

		if not self.block_winner[move_b]:
			for position in xrange(16):
				if self.checkX(self.board[move_b], position) or self.checkO(self.board[move_b], position):
					pass
				else:
					possible = True
					new_x, new_y = (move_bx << 2) + (position >> 2), (move_by << 2) + (position & 3) 
					valid_moves.append((new_x, new_y))

		if possible:
			return valid_moves

		for move_b in xrange(16):
			if self.block_winner[move_b] == 0:
				(move_bx, move_by) = (move_b >> 2, move_b & 3) 
				for position in xrange(16):
					if self.checkX(self.board[move_b], position) or self.checkO(self.board[move_b], position):
						pass
					else:
						possible = True
						new_x, new_y = (move_bx << 2) + (position >> 2), (move_by << 2) + (position & 3) 
						valid_moves.append((new_x, new_y))

		return valid_moves				

	def try_update(self, current_move):
		(cur_x, cur_y) = (current_move[0], current_move[1])
		(cur_bx, cur_by) = (cur_x >> 2, cur_y >> 2)
		cur_block = (cur_bx << 2) + cur_by
		(cur_posx, cur_posy) = (cur_x & 3, cur_y & 3)
		cell = (cur_posy + (cur_posx << 2))

		self.board[cur_block] |= (1 << (cell << 1))
		self.zobrist_hash ^= self.zobrist_values[0][(cur_x << 4) + cur_y]

		if match_win(cur_block):
			self.block_winner[cur_block] = 1
		elif match_loss(cur_block):
			self.block_winner[cur_block] = 2
		else:
			self.block_winner[cur_block] = 0

		if self.block_winner[cur_block]:
			return True
		else:
			return False

	def try_revert(self, current_move):
		(cur_x, cur_y) = (current_move[0], current_move[1])
		(cur_bx, cur_by) = (cur_x >> 2, cur_y >> 2)
		cur_block = (cur_bx << 2) + cur_by
		(cur_posx, cur_posy) = (cur_x & 3, cur_y & 3)
		cell = (cur_posy + (cur_posx << 2))

		self.board[cur_block] -= (1 << (cell << 1))
		self.zobrist_hash ^= self.zobrist_values[0][(cur_x << 4) + cur_y]

		if match_win(cur_block):
			self.block_winner[cur_block] = 1
		elif match_loss(cur_block):
			self.block_winner[cur_block] = 2
		else:
			self.block_winner[cur_block] = 0


	def minimax(self, depth, alpha, beta, isMaximizing, old_move, current_hash, bonus_used):
		# check terminal state here

		if depth == 0:
			return randint(-MAX_VAL, MAX_VAL)

		if (current_hash, isMaximizing, bonus_used) in self.cached_states:
			return self.cached_states[(current_hash, isMaximizing, bonus_used)]

		valid_moves = self.getValidMoves(old_move)

		if not len(valid_moves):
			return randint(-MAX_VAL, MAX_VAL)

		new_val = 0
		if isMaximizing:
			new_val = -MAX_VAL
			for current_move in valid_moves:
				# update changes in global variables here
				win_block = self.try_update(current_move)

				if win_block and not bonus_used:
					t_val = self.minimax(depth - 1, alpha, beta, isMaximizing, current_move, self.zobrist_hash, True)
				else:
					t_val = self.minimax(depth - 1, alpha, beta, not isMaximizing, current_move, self.zobrist_hash, False)

				if t_val > new_val:
					if self.level == depth:
						# print "YES"
						# print current_move[0] & 3, current_move[1] & 3
						self.best_move = current_move
					new_val = t_val

				if alpha < new_val:
					alpha = new_val

				# revert changes in global variables here
				self.try_revert(current_move)

				if beta <= alpha:
					break
		
		else:
			new_val = MAX_VAL
			for current_move in valid_moves:
				# update changes in global variables here
				win_block = self.try_update(current_move)

				if win_block and not bonus_used:
					t_val = self.minimax(depth - 1, alpha, beta, isMaximizing, current_move, self.zobrist_hash, True)
				else:
					t_val = self.minimax(depth - 1, alpha, beta, not isMaximizing, current_move, self.zobrist_hash, False)

				if t_val < new_val:
					if self.level == depth:
						# print "YES"
						# print current_move[0] & 3, current_move[1] & 3
						self.best_move = current_move
					new_val = t_val

				if beta > new_val:
					beta = new_val

				# revert changes in global variables here
				self.try_revert(current_move)

				if beta <= alpha:
					break

		self.cached_states[(current_hash, isMaximizing, bonus_used)] = new_val
		return new_val

	def print_board(self, board):
		print "current board"
		for x in xrange(16):
			for y in xrange(16):
				print board.board_status[x][y],
				if y and (y%4 == 3):
					print " ",
			if x and (x%4 == 3):
				print ""
			print ""
		

	def update(self, board, my_symbol):
	
		# self.print_board(board)		
		self.zobrist_hash = 0
		
		for current_block in xrange(16):
			self.board[current_block] = 0
			(block_x, block_y) = (current_block >> 2, current_block & 3)
			for x in xrange(4):
				for y in xrange(4):
					(abs_x, abs_y) = ((block_x << 2) + x, (block_y << 2) + y)
					if board.board_status[abs_x][abs_y] == '-':
						pass
					elif board.board_status[abs_x][abs_y] == my_symbol:
						self.zobrist_hash ^= self.zobrist_values[0][(abs_x << 4) + abs_y]
						self.board[current_block] |= (1 << (((x << 2) + y) << 1))
					else:
						self.zobrist_hash ^= self.zobrist_values[1][(abs_x << 4) + abs_y]
						self.board[current_block] |= (1 << ((((x << 2) + y) << 1) + 1))			
			if match_win(self.board[current_block]):
				self.block_winner[current_block] = 1
			elif match_loss(self.board[current_block]):
				self.block_winner[current_block] = 2
			else:
				self.block_winner[current_block] = 0

	def move(self, board, old_move, flag):

		cur_time = time.time()

		self.update(board, flag)

		signal.signal(signal.SIGALRM, self.signal_handler)
		signal.alarm(15)

		# print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"
		# print "last move", old_move

		(last_x, last_y) = (old_move[0], old_move[1])
		current_move = (-1, -1)

		if (last_x, last_y) != (-1, -1):
			(row, col) = (last_x >> 2, last_y >> 2)
			last_block = (row << 2) + col
			(last_posx, last_posy) = (last_x & 3, last_y & 3)
			cell = (last_posy + (last_posx << 2))
			current_move = self.getValidMoves(old_move)
			current_move = current_move[0]
		else:
			# starting move
			current_move = ((0, 0))

		# print cur_time

		for depth in xrange(3, 6, 2):
			print depth
			self.cached_states = {}
			self.level = depth
			self.minimax(depth, -MAX_VAL, MAX_VAL, 1, old_move, self.zobrist_hash, self.last_win)
			current_move = self.best_move

		# depth = 3
		# while time.time() - cur_time < 10:
		# 	print time.time() - cur_time
		# 	self.cached_states = {}
		# 	self.level = depth
		# 	self.minimax(depth, -MAX_VAL, MAX_VAL, 1, old_move, self.zobrist_hash, self.last_win)
		# 	current_move = self.best_move
		# 	depth = depth + 1
		# 	# print time.time() - cur_time
		# 	print depth
		# 	# if depth > 7:
		# 	# 	break

		# print "old move", old_move
		# print "cur move", current_move


		(cur_x, cur_y) = (current_move[0], current_move[1])
		(cur_bx, cur_by) = (cur_x >> 2, cur_y >> 2)
		cur_block = (cur_bx << 2) + cur_by
		(cur_posx, cur_posy) = (cur_x & 3, cur_y & 3)
		cell = (cur_posy + (cur_posx << 2))

		prev_win = match_win(cur_block)
		self.board[cur_block] |= (1 << (cell << 1))
		if not prev_win and match_win(cur_block):
			self.last_win = True
		else:
			self.last_win = False

		return current_move
