# 01 -> X
# 10 -> Y

import numpy as np

states = {} 

MAX = (1 << 20)
LIM = (1 << 32) - 1

def checkX(mask, pos):
	if (mask & (1 << (pos + pos))) and ((mask & (1 << (pos + pos + 1))) == 0):
		return True
	return False

def checkO(mask, pos):
	if (mask & (1 << (pos + pos + 1))) and ((mask & (1 << (pos + pos))) == 0):
		return True
	return False

def match_win(mask):
	for i in xrange(0, 3):
		if checkX(mask, 4 * i) and checkX(mask, 4 * i + 1) and checkX(mask, 4 * i + 2) and checkX(mask, 4 * i + 3):
			return True
		if checkX(mask, i) and checkX(mask, i + 4) and checkX(mask, i + 8) and checkX(mask, i + 12):
			return True

	if checkX()

	return False 

def solve(mask):

	if mask in states:
		return states[mask]
	if match_win(mask):
		return states[mask] = MAX
	elif match_loss(mask):
		return states[mask] = 0
	elif match_draw(mask):
		return states[mask] = 0

	ans = 0
	for i in xrange(0, 15):
		X = 1 << (i + i)
		Y = 1 << (i + i + 1)
		if (mask & X) and (mask & Y):
			new_mask = mask - X 
			ans = solve(new_mask) + solve(new_mask ^ LIM)
		elif (mask & X):
			pass
		elif (mask & Y):
			pass
		else:
			new_mask = mask | X
			ans = solve(new_mask) + solve(new_mask ^ LIM)
	states[mask] = ans
	return ans

print solve(0)