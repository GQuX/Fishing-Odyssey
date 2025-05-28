FISHING_POLE_SLOT = '7'
CAST_WAIT = 11 # seconds
CAST_TIMEOUT = 60 # seconds (whole number)
CLICK_COUNT = 85 # when reeling in click _ times
WHITE_LEVEL = 200 # 1-255

FOOD_SLOT = '4'
FOOD_INTERVAL = 20 # minutes

###############################################################################################################################################################################

from time import sleep, perf_counter
from ahk import AHK; ahk = AHK() #ahk | "ahk[binary]"
from desktopmagic.screengrab_win32 import getRectAsImage #desktopmagic | pywin32 | pillow

###############################################################################################################################################################################

class Window:
	def __init__(self):
		self.window = ahk.win_get(title="Roblox")
		assert self.window, "Failed to find Roblox window."
		
		self.x, self.y, self.width, self.height = self.window.get_position()

	def Activate(self):
		assert self.window, "Failed to find Roblox window."
		self.window.activate()

	def CastRod(self):
		print("\nCasting Rod..")
		self.Activate()

		ahk.mouse_move(
			x = self.width  * 0.5,
			y = self.height * 0.3, 
			speed = 2 )
		sleep(0.3)

		ahk.click(click_count=1)

	def AlertOnScreen(self) -> bool:
		img = getRectAsImage((
			int(self.x + (self.width  * 0.5)),
			int(self.y + (self.height * 0.3)),
			int(self.x + (self.width  * 0.5)) + 1,
			int(self.y + (self.height * 0.5)) ))
		img = img.convert('L')
		
		pixels = img.load()
		for y in range(img.size[1]-1, -1, -5):
			if pixels[0, y] > WHITE_LEVEL: return True
		return False
	
	def WaitForAlert(self):
		sleep(CAST_WAIT)
		print("Waiting... ", end="")
		num_checks = (CAST_WAIT*2)
		while not self.AlertOnScreen():
			sleep(0.5)
			num_checks += 1
			if num_checks >= (CAST_TIMEOUT*2): break
		print(f"({num_checks/2})")

	def ReelIn(self):
		self.Activate()

		ahk.mouse_move(
			x = self.width  * 0.5,
			y = self.height * 0.3, 
			speed = 2 )
		sleep(0.1)

		for _ in range(CLICK_COUNT):
			ahk.click()
			sleep(0.05)

		print("Hopefully I Caught Something Cool.")

###############################################################################################################################################################################

def Run():
	print("Running Arcane Odyssey Auto Fisher.\n")
	client = Window()
	client.Activate()
	eat_time = perf_counter() + (60 * FOOD_INTERVAL)

	while True:
		ahk.key_press(FISHING_POLE_SLOT)
		
		client.CastRod()
		client.WaitForAlert()
		client.ReelIn()

		if perf_counter() > eat_time:
			eat_time += (60 * FOOD_INTERVAL)
			ahk.key_press(FOOD_SLOT)
			ahk.click()
			sleep(0.25)
		else:
			ahk.key_press(FISHING_POLE_SLOT)
		sleep(0.5)

Run()