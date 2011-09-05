# TODO: make these better, maybe add a generator for them, and make like 2 dozen more
# also make them rotate
from play import point

class Template(object):
	def __init__(self, pattern, swap):
		self.pattern = pattern
		self.swap = swap
		self.maxedge()

	def maxedge(self):
		x = 0
		y = 0
		for p in self.pattern:
			if p.a > x:
				x = p.a
			if p.b > y:
				y = p.b
		self.edge = (7-x, 7-y)

	def search(self, grid):
		possibles = []
		for x in xrange(self.edge[0]+1):
			for y in xrange(self.edge[1]+1):
				g = point(x, y)
				points = [grid[g+p] for p in self.pattern]
				#if len(list(dropwhile(lambda x: x==grid[g+t[0]], points))) <= 1:
				if all([p == grid[g+self.pattern[0]] for p in points]):
					possibles.append(((self.swap[0]+g).tuple(), (self.swap[1]+g).tuple()))
		return possibles
	def __repr__(self):
		return '''Template({0},
						{1})'''.format(self.pattern, self.swap)
# this is what i want a template to look like
# A is the gem we'll be moving; b is the spot we'll switch it with
# Xs are gems that match A
# -s are anything
'''
Ab
-X
-X
'''

def rotate_90(p):
	x = -p.b
	y =  p.a
	return point(x, y)

def reflecth(p):
	x = -p.a
	y = p.b
	return point(x, y)

def alter_template(f, t):
	newtemp = map(f, t.pattern)
	newswap = map(f, t.swap)
	hadjust = 0
	vadjust = 0
	for p in newtemp:
		if p.a < hadjust:
			hadjust = p.a
		if p.b < vadjust:
			vadjust = p.b
	shift = point(-hadjust, -vadjust)
	newtemp = map(shift.__add__, newtemp)
	newswap = map(shift.__add__, newswap)
	return Template(newtemp, newswap)

def full_coverage(t): # for full coverage, rotate 4 times, mirror, rotate 4 more times?
	temps = [t]
	rotation = t
	for x in xrange(4):
		rotation = alter_template(rotate_90, rotation)
		temps.append(rotation)
		temps.append(alter_template(reflecth, rotation))
	return temps

def parse_template(art):
	art = art.strip('\n')
	tplate = []
	swap = []
	for y, line in enumerate(art.split('\n')):
		for x, char in enumerate(line.strip()):
			if char in ('X', 'A'):
				tplate.append(point(x, y))
			if char in ('A', 'b'):
				swap.append(point(x, y))
	return Template(tplate, swap)

def load_templates(data):
	data = data.strip('\n')
	arts = data.split('\n\n')
	temps = []
	for a in arts:
		temps += full_coverage(parse_template(a))
	return temps

templates = load_templates(file('templates.txt', 'r').read())