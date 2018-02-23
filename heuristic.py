# 01 -> X
# 10 -> Y

import numpy as np

states = {}
cur_state = [0] * 16

MAX = (1 << 20)

def checkX(mask, pos):
	return (mask & (1 << (pos + pos))) != 0

def checkO(mask, pos):
	return (mask & (1 << (pos + pos + 1))) != 0

def flipboard(mask):
	for i in xrange(16):
		if checkX(mask, i) or checkO(mask, i)
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
		states[mask] = np.uint32(MAX)
		return MAX
	elif match_draw(mask):
		states[mask] = np.uint32(0)
		return 0

	ans = np.uint32(0)

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

	states[mask] = ans
	return states[mask]

print solve(0)