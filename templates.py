# TODO: make these better, maybe add a generator for them, and make like 2 dozen more
# also make them rotate

from play import point

class Template(object):
	def __init__(self, pattern, swap, edge):
		self.pattern = pattern
		self.swap = swap
		self.edge = edge

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
#this is what i want a template to look like
'''
Ab
-X
-X
'''

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
	edgex = max(map(lambda x:len(x.strip()), art.split('\n')))
	edgey = len(art.split('\n'))
	return Template(tplate, swap, (8-edgex, 8-edgey))

templates = [
parse_template(
'''
Ab
-X
-X
'''),
parse_template(
'''
-X
-X
Ab
'''),
parse_template(
'''
X
X
bA
'''),
parse_template(
'''
A
b
X
X
'''),
parse_template(
'''
X
X
b
A
'''),
parse_template(
'AbXX'),
parse_template(
'XXbA'),
parse_template(
'''
bA
X-
X-
'''),
parse_template(
'''
--A
XXb
'''),
parse_template(
'''
XXb
--A
'''),
parse_template(
'''
bXX
A
'''),
parse_template(
'''
XbX
-A
'''),
parse_template(
'''
-A
XbX
'''),
parse_template(
'''
X
bA
X
'''),
parse_template(
'''
-X
Ab
-X
'''),
parse_template(
'''
A
bXX
'''),
]
