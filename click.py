import ctypes
from PIL import ImageGrab

class Rect(ctypes.Structure):
	_fields_ = [('left', ctypes.c_long),
				('top', ctypes.c_long),
				('right', ctypes.c_long),
				('bottom', ctypes.c_long)
	]
	def packed_coords(self):
		return (self.left, self.top, self.right, self.bottom)

user32 = ctypes.windll.user32

HWND = user32.FindWindowA(None, "Bejeweled 3")

bbox = Rect() # this variable is IMPORTANT
user32.GetWindowRect(HWND, ctypes.byref(bbox))

def get_screen():
	return ImageGrab.grab(bbox.packed_coords())

class MouseInput(ctypes.Structure): #this is actually an INPUT struct with a MOUSEINPUT where the union should be
	_fields_ = [('type', ctypes.c_ulong), #this should always be 0
				('dx', ctypes.c_long),
				('dy', ctypes.c_long),
				('mouseData', ctypes.c_ulong),
				('dwFlags', ctypes.c_ulong),
				('time', ctypes.c_ulong),
				('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong))
	]

ScreenWidth = 1280
ScreenHeight = 1024

def send_click(x, y):
	clickarray = (MouseInput * 3)()
	clickarray[0] = MouseInput()
	clickarray[0].dx = x*(65335/ScreenWidth)
	clickarray[0].dy = y*(65335/ScreenHeight)
	clickarray[0].dwFlags = 0x0001 | 0x8000 # MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
	clickarray[1] = MouseInput()
	clickarray[1].dx = x*(65335/ScreenWidth)
	clickarray[1].dy = y*(65335/ScreenHeight)
	clickarray[1].dwFlags = 0x0002 # MOUSEEVENTF_LEFTDOWN
	clickarray[2] = MouseInput()
	clickarray[2].dx = x*(65335/ScreenWidth)
	clickarray[2].dy = y*(65335/ScreenHeight)
	clickarray[2].dwFlags = 0x0004 # MOUSEEVENTF_LEFTUP

	user32.SendInput(3, clickarray, ctypes.sizeof(MouseInput))

grid_offset = (350, 92)
grid_square = 82
def swap_gems(gem1, gem2):
	print 'clicking at', gem1, gem2
	gem1 = map(lambda x:x*grid_square, gem1)
	gem2 = map(lambda x:x*grid_square, gem2)
	gem1[0] += grid_offset[0]+bbox.left
	gem1[1] += grid_offset[1]+bbox.top
	gem2[0] += grid_offset[0]+bbox.left
	gem2[1] += grid_offset[1]+bbox.top
	send_click(*gem1)
	send_click(*gem2)