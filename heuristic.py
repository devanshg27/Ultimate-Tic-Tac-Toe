# 01 -> X
# 10 -> Y

states = {}
cur_state = [1] * 16

MAX = (1 << 20)

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

def match_draw(mask):
	# Rows and columns
	cnt = 0
	if checkO(mask, 0) or checkO(mask, 0 + 1) or checkO(mask, 0 + 2) or checkO(mask, 0 + 3):
		cnt += 1
	if checkO(mask, 0) or checkO(mask, 0 + 4) or checkO(mask, 0 + 8) or checkO(mask, 0 + 12):
		cnt += 1

	if checkO(mask, 4) or checkO(mask, 4 + 1) or checkO(mask, 4 + 2) or checkO(mask, 4 + 3):
		cnt += 1
	if checkO(mask, 1) or checkO(mask, 1 + 4) or checkO(mask, 1 + 8) or checkO(mask, 1 + 12):
		cnt += 1

	if checkO(mask, 8) or checkO(mask, 8 + 1) or checkO(mask, 8 + 2) or checkO(mask, 8 + 3):
		cnt += 1
	if checkO(mask, 2) or checkO(mask, 2 + 4) or checkO(mask, 2 + 8) or checkO(mask, 2 + 12):
		cnt += 1

	if checkO(mask, 12) or checkO(mask, 12 + 1) or checkO(mask, 12 + 2) or checkO(mask, 12 + 3):
		cnt += 1
	if checkO(mask, 3) or checkO(mask, 3 + 4) or checkO(mask, 3 + 8) or checkO(mask, 3 + 12):
		cnt += 1
	# Diamonds
	if checkO(mask, 1) or checkO(mask, 1 + 3) or checkO(mask, 1 + 5) or checkO(mask, 1 + 8):
		cnt += 1
	if checkO(mask, 2) or checkO(mask, 2 + 3) or checkO(mask, 2 + 5) or checkO(mask, 2 + 8):
		cnt += 1
	if checkO(mask, 5) or checkO(mask, 5 + 3) or checkO(mask, 5 + 5) or checkO(mask, 5 + 8):
		cnt += 1
	if checkO(mask, 6) or checkO(mask, 6 + 3) or checkO(mask, 6 + 5) or checkO(mask, 6 + 8):
		cnt += 1
	return (cnt == 12)

def solve(mask):
	if mask in states:
		return states[mask]
	if match_win(mask):
		states[mask] = (MAX)
		return MAX
	elif match_draw(mask):
		states[mask] = (0)
		return 0

	ans = (0)

	if checkO(mask, 0) or checkO(mask, 0 + 1) or checkO(mask, 0 + 2) or checkO(mask, 0 + 3):
		pass
	else:
		num = checkX(mask, 0) + checkX(mask, 0 + 1) + checkX(mask, 0 + 2) + checkX(mask, 0 + 3)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 0) or checkO(mask, 0 + 4) or checkO(mask, 0 + 8) or checkO(mask, 0 + 12):
		pass
	else:
		num = checkX(mask, 0) + checkX(mask, 0 + 4) + checkX(mask, 0 + 8) + checkX(mask, 0 + 12)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))

	if checkO(mask, 4) or checkO(mask, 4 + 1) or checkO(mask, 4 + 2) or checkO(mask, 4 + 3):
		pass
	else:
		num = checkX(mask, 4) + checkX(mask, 4 + 1) + checkX(mask, 4 + 2) + checkX(mask, 4 + 3)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 1) or checkO(mask, 1 + 4) or checkO(mask, 1 + 8) or checkO(mask, 1 + 12):
		pass
	else:
		num = checkX(mask, 1) + checkX(mask, 1 + 4) + checkX(mask, 1 + 8) + checkX(mask, 1 + 12)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))

	if checkO(mask, 8) or checkO(mask, 8 + 1) or checkO(mask, 8 + 2) or checkO(mask, 8 + 3):
		pass
	else:
		num = checkX(mask, 8) + checkX(mask, 8 + 1) + checkX(mask, 8 + 2) + checkX(mask, 8 + 3)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 2) or checkO(mask, 2 + 4) or checkO(mask, 2 + 8) or checkO(mask, 2 + 12):
		pass
	else:
		num = checkX(mask, 2) + checkX(mask, 2 + 4) + checkX(mask, 2 + 8) + checkX(mask, 2 + 12)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))

	if checkO(mask, 12) or checkO(mask, 12 + 1) or checkO(mask, 12 + 2) or checkO(mask, 12 + 3):
		pass
	else:
		num = checkX(mask, 12) + checkX(mask, 12 + 1) + checkX(mask, 12 + 2) + checkX(mask, 12 + 3)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 3) or checkO(mask, 3 + 4) or checkO(mask, 3 + 8) or checkO(mask, 3 + 12):
		pass
	else:
		num = checkX(mask, 3) + checkX(mask, 3 + 4) + checkX(mask, 3 + 8) + checkX(mask, 3 + 12)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	# Diamonds
	if checkO(mask, 1) or checkO(mask, 1 + 3) or checkO(mask, 1 + 5) or checkO(mask, 1 + 8):
		pass
	else:
		num = checkX(mask, 1) + checkX(mask, 1 + 3) + checkX(mask, 1 + 5) + checkX(mask, 1 + 8)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 2) or checkO(mask, 2 + 3) or checkO(mask, 2 + 5) or checkO(mask, 2 + 8):
		pass
	else:
		num = checkX(mask, 2) + checkX(mask, 2 + 3) + checkX(mask, 2 + 5) + checkX(mask, 2 + 8)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 5) or checkO(mask, 5 + 3) or checkO(mask, 5 + 5) or checkO(mask, 5 + 8):
		pass
	else:
		num = checkX(mask, 5) + checkX(mask, 5 + 3) + checkX(mask, 5 + 5) + checkX(mask, 5 + 8)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))
	if checkO(mask, 6) or checkO(mask, 6 + 3) or checkO(mask, 6 + 5) or checkO(mask, 6 + 8):
		pass
	else:
		num = checkX(mask, 6) + checkX(mask, 6 + 3) + checkX(mask, 6 + 5) + checkX(mask, 6 + 8)
		ans	+= (MAX >> (((4 - num)*(5 - num))>>1))

	states[mask] = (ans*1.0)/2**15
	return states[mask]

def heur():
	ans = 0
	ans += solve(cur_state[0]) * solve(cur_state[0 + 1]) * solve(cur_state[0 + 2]) * solve(cur_state[0 + 3])
	ans -= solve(flipboard(cur_state[0])) * solve(flipboard(cur_state[0 + 1])) * solve(flipboard(cur_state[0 + 2])) * solve(flipboard(cur_state[0 + 3]))

	ans += solve(cur_state[0]) * solve(cur_state[0 + 4]) * solve(cur_state[0 + 8]) * solve(cur_state[0 + 12])
	ans -= solve(flipboard(cur_state[0])) * solve(flipboard(cur_state[0 + 4])) * solve(flipboard(cur_state[0 + 8])) * solve(flipboard(cur_state[0 + 12]))


	ans += solve(cur_state[4]) * solve(cur_state[4 + 1]) * solve(cur_state[4 + 2]) * solve(cur_state[4 + 3])
	ans -= solve(flipboard(cur_state[4])) * solve(flipboard(cur_state[4 + 1])) * solve(flipboard(cur_state[4 + 2])) * solve(flipboard(cur_state[4 + 3]))

	ans += solve(cur_state[1]) * solve(cur_state[1 + 4]) * solve(cur_state[1 + 8]) * solve(cur_state[1 + 12])
	ans -= solve(flipboard(cur_state[1])) * solve(flipboard(cur_state[1 + 4])) * solve(flipboard(cur_state[1 + 8])) * solve(flipboard(cur_state[1 + 12]))


	ans += solve(cur_state[8]) * solve(cur_state[8 + 1]) * solve(cur_state[8 + 2]) * solve(cur_state[8 + 3])
	ans -= solve(flipboard(cur_state[8])) * solve(flipboard(cur_state[8 + 1])) * solve(flipboard(cur_state[8 + 2])) * solve(flipboard(cur_state[8 + 3]))

	ans += solve(cur_state[2]) * solve(cur_state[2 + 4]) * solve(cur_state[2 + 8]) * solve(cur_state[2 + 12])
	ans -= solve(flipboard(cur_state[2])) * solve(flipboard(cur_state[2 + 4])) * solve(flipboard(cur_state[2 + 8])) * solve(flipboard(cur_state[2 + 12]))


	ans += solve(cur_state[12]) * solve(cur_state[12 + 1]) * solve(cur_state[12 + 2]) * solve(cur_state[12 + 3])
	ans -= solve(flipboard(cur_state[12])) * solve(flipboard(cur_state[12 + 1])) * solve(flipboard(cur_state[12 + 2])) * solve(flipboard(cur_state[12 + 3]))

	ans += solve(cur_state[3]) * solve(cur_state[3 + 4]) * solve(cur_state[3 + 8]) * solve(cur_state[3 + 12])
	ans -= solve(flipboard(cur_state[3])) * solve(flipboard(cur_state[3 + 4])) * solve(flipboard(cur_state[3 + 8])) * solve(flipboard(cur_state[3 + 12]))

	# Diamonds
	ans += solve(cur_state[1]) * solve(cur_state[1 + 3]) * solve(cur_state[1 + 5]) * solve(cur_state[1 + 8])
	ans -= solve(flipboard(cur_state[1])) * solve(flipboard(cur_state[1 + 3])) * solve(flipboard(cur_state[1 + 5])) * solve(flipboard(cur_state[1 + 8]))

	ans += solve(cur_state[2]) * solve(cur_state[2 + 3]) * solve(cur_state[2 + 5]) * solve(cur_state[2 + 8])
	ans -= solve(flipboard(cur_state[2])) * solve(flipboard(cur_state[2 + 3])) * solve(flipboard(cur_state[2 + 5])) * solve(flipboard(cur_state[2 + 8]))

	ans += solve(cur_state[5]) * solve(cur_state[5 + 3]) * solve(cur_state[5 + 5]) * solve(cur_state[5 + 8])
	ans -= solve(flipboard(cur_state[5])) * solve(flipboard(cur_state[5 + 3])) * solve(flipboard(cur_state[5 + 5])) * solve(flipboard(cur_state[5 + 8]))

	ans += solve(cur_state[6]) * solve(cur_state[6 + 3]) * solve(cur_state[6 + 5]) * solve(cur_state[6 + 8])
	ans -= solve(flipboard(cur_state[6])) * solve(flipboard(cur_state[6 + 3])) * solve(flipboard(cur_state[6 + 5])) * solve(flipboard(cur_state[6 + 8]))

	return ans

def heur_draw():
	ans = solve(0) * 6 + solve(1) * 4 + solve(2) * 4 + solve(3) * 6
	ans += solve(4+0) * 4 + solve(4+1) * 3 + solve(4+2) * 3 + solve(4+3) * 4
	ans += solve(8+0) * 4 + solve(8+1) * 3 + solve(8+2) * 3 + solve(8+3) * 4
	ans += solve(12+0) * 6 + solve(12+1) * 4 + solve(12+2) * 4 + solve(12+3) * 6
	return ans

def evaluation():
	if match_win(cur_win_state):
		return 2**30
	if match_loss(cur_win_state):
		return -2**30
	return heur()

def evaluation_draw():
	if match_loss(cur_win_state):
		return -2**30
	return heur_draw()