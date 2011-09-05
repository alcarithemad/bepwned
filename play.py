import click, colors, templates

class point(object):
	def __init__(self, a, b):
		self.a, self.b = a, b
	def __add__(self, p):
		return point(self.a+p.a, self.b+p.b)
	def tuple(self):
		return (self.a, self.b)
	def __str__(self):
		return '({0}, {1})'.format(self.a, self.b)

class Grid(object):
	gleft = click.grid_offset[0]
	gtop = click.grid_offset[1]
	gright = gleft+(click.grid_square*8)
	gbottom = gtop+(click.grid_square*8)
	def __init__(self, imagefunc):
		self.grid = [[0]*8 for x in xrange(8)]
		self.imagefunc = imagefunc

	def __getitem__(self, p):
		#print self.grid[p.a][p.b]
		return self.grid[p.a][p.b]
	
	def updategrid(self):
		img = self.imagefunc()
		img = img.crop((self.gleft, self.gtop, self.gright, self.gbottom))
		img = img.load()
		for x in xrange(len(self.grid)):
			for y in xrange(len(self.grid[0])):
				#points = [(x*click.grid_square+a, y*click.grid_square+b) for b in xrange(79) 
				#			for a in xrange(79) 
				#				if any(map(lambda x: x>=130, img[x*click.grid_square+a, y*click.grid_square+b]))]
				#color = map(lambda p: img[p[0], p[1]], points)
				#avgcolor = map(lambda x:x/len(points), map(sum, zip(*color)))
				color = img[x*click.grid_square+36,y*click.grid_square+50]
				avgcolor =map(lambda x:x/55, map(sum, zip(color)))
				#avgcolor = colors.normalizeColor(color)
				#print avgcolor
				if (x,y) in ((2, 2,), (0, 1)):
					pass
					#print avgcolor
					#print colors.normalizeColor(avgcolor)	
				self.grid[x][y] = avgcolor
	
	def search(self, func):
		func(self)

if __name__ == '__main__':
	click.user32.BringWindowToTop(click.HWND)
	click.user32.SetForegroundWindow(click.HWND)
	g = Grid(click.get_screen)
	import random, time
	random.seed()
	matches = 0
	while matches < 600:
		g.updategrid()
		choices = []
		for t in templates.templates:		
			choices += t.search(g)
		#random.shuffle(choices)
		for c in choices:
			click.swap_gems(*c)
			matches += 1
		time.sleep(.1)
	print 'ps', (g[point(0, 4)], g[point(0, 6)], g[point(0, 7)])
	# for x in xrange(2):
	# 	first = random.randint(1, 6), random.randint(1, 6)
	# 	if random.random() > 0.5:
	# 		second = first[0]+random.choice((-1, 1)), first[1]
	# 	else:
	# 		second = first[0], first[1]+random.choice((-1, 1))
	# 	click.swap_gems(first, second)
	#click.swap_gems((4, 3), (5, 3))
