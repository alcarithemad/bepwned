from itertools import dropwhile
import click

class point(object):
	def __init__(self, a, b):
		self.a, self.b = a, b
	def __add__(self, p):
		return point(self.a+p.a, self.b+p.b)
	def tuple(self):
		return (self.a, self.b)

class Grid(object):
	gleft = click.grid_offset[0]
	gtop = click.grid_offset[1]
	gright = gleft+(click.grid_square*8)
	gbottom = gtop+(click.grid_square*8)
	def __init__(self, imagefunc):
		self.grid = [[0]*8 for x in xrange(8)]
		self.imagefunc = imagefunc

	def __getitem__(self, p):
		print self.grid[p.a][p.b]
		return self.grid[p.a][p.b]
	
	def updategrid(self):
		img = self.imagefunc()
		img.crop((self.gleft, self.gtop, self.gright, self.gbottom))
		img = img.load()
		for x in xrange(len(self.grid)):
			for y in xrange(len(self.grid[0])):
				points = [(x*click.grid_square+a, y*click.grid_square+b) for b in xrange(82) for a in xrange(82)]
				colors = map(lambda p: img[p[0], p[1]], points)
				avgcolor = map(lambda x:x/len(points), map(sum, zip(*colors)))
				#print avgcolor
				if (x,y) in ((2,6), (2, 4)):
					print avgcolor
				self.grid[x][y] = avgcolor
	
	def search(self, func):
		func(self)

tplates = [(
			(point(1, 0), point(0, 1), point(1, 2)),	# if these are all the same,
			(point(0, 1), point(1, 1)),					# swap these
			(6, 4)	# edge
			),
			(
			(point(0, 0), point(0, 2), point(0, 3)),	# if these are all the same,
			(point(0, 0), point(0, 1)),					# swap these
			(7, 4)	# edge
			),
			(
			(point(0, 0), point(1, 0), point(3, 0)),	# if these are all the same,
			(point(3, 0), point(2, 0)),					# swap these
			(4, 7)	# edge
			),
			(
			(point(1, 0), point(2, 0), point(0, 1)),	# if these are all the same,
			(point(0, 0), point(0, 1)),					# swap these
			(4, 6)	# edge
			)
		]
def template(tplate):
	t = tplate[0]
	swap = tplate[1]
	edge = tplate[2]
	def f(grid):
		for x in xrange(edge[0]+1):
			for y in xrange(edge[1]+1):
				g = point(x, y)
				points = [grid[g+p] for p in t]
				if len(list(dropwhile(lambda x: x==grid[g+t[0]], points))) > 1:
					click.swap_gems((swap[0]+g).tuple(), (swap[1]+g).tuple())
	return f
					

if __name__ == '__main__':
	click.user32.BringWindowToTop(click.HWND)
	click.user32.SetForegroundWindow(click.HWND)
	g = Grid(click.get_screen)
	g.updategrid()
	for t in tplates:
		f = template(t)
		g.search(f)
	print 'ps', (g[point(0, 4)], g[point(0, 6)], g[point(0, 7)])
	# import random
	# for x in xrange(2):
	# 	first = random.randint(1, 6), random.randint(1, 6)
	# 	if random.random() > 0.5:
	# 		second = first[0]+random.choice((-1, 1)), first[1]
	# 	else:
	# 		second = first[0], first[1]+random.choice((-1, 1))
	# 	click.swap_gems(first, second)
	#swap_gems((4, 3), (5, 3))
