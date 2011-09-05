import math

rgbColor = {'black' : (0,   0,   0  ),
			'white' : (255, 255, 255),
			'green' : (0,   255, 0  ),
			'red'   : (255, 0,   0  ),
			'blue'  : (0,   0,   255),
			'yellow': (255, 255, 0  ),
			'orange': (255, 165, 0  ),
			'violet': (128, 0,   128)}

def distance(x,y):
	return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2)

def normalizeColor(rgb):
	lowestvalue = 450
	lowestkey = 'black'
	for key, value in rgbColor.items():
		d = distance(rgb, value)
		if d < lowestvalue:
			lowestvalue, lowestkey = d, key

	return lowestkey

def getColors(img):
	colors = []
	for x in xrange(8):
		colors.append([])
		for y in xrange(8):
			color = img.getpixel((x*95+35,y*95+55))
			color = normalizeColor(color)
			colors[x].append(color)
	return colors