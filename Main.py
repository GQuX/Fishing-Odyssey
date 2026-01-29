from typing import cast
from dataclasses import dataclass
from time import sleep, perf_counter
from ahk import AHK; ahk = AHK() # install: ahk | "ahk[binary]"
from PIL import Image as PILImage # type: ignore # install: pillow
from desktopmagic.screengrab_win32 import getRectAsImage as capture_region # type: ignore # install: desktopmagic | pywin32

# ── Config ────────────────────────────────────────────────────────────────── #

FISHING_POLE_SLOT = '7' # 0-9
CAST_WAIT = 11 # seconds
CAST_TIMEOUT = 60 # seconds (whole number)
CLICK_COUNT = 85 # when reeling in click _ times
WHITE_LEVEL = 200 # 1-255

FOOD_SLOT = '4'
FOOD_INTERVAL = 20 # minutes

# ── Window ────────────────────────────────────────────────────────────────── #

@dataclass(slots = True)
class Dimensions:
	x: int
	y: int
	width:  int
	height: int

	@property
	def center_x(self) -> int:
		return self.x + self.width // 2
	
	@property
	def alert_top(self) -> int:
		return self.y + int(self.height * 0.3)
	
	@property
	def alert_bottom(self) -> int:
		return self.y + int(self.height * 0.5)

class Window:
	def __init__(self) -> None:
		window = ahk.win_get(title = "Roblox")
		assert window is not None, "Failed to find Roblox window"
		self._window = window
		self.refresh_dimensions()

	def refresh_dimensions(self) -> None:
		x, y, w, h = cast(tuple[int, int, int, int], self._window.get_position())
		self.dimensions = Dimensions(x, y, w, h)

	def activate(self) -> None:
		self._window.activate()

	def center_mouse(self, wait_time: float = 0.1):
		self.refresh_dimensions()
		ahk.mouse_move(
			x = self.dimensions.center_x,
			y = self.dimensions.alert_top, 
			speed = 2 )
		sleep(wait_time)

	def cast_rod(self):
		print("\nCasting rod..")
		self.activate()
		self.center_mouse(0.3)
		ahk.click(click_count = 1)

	def _capture_alert_region(self) -> PILImage.Image:
		self.refresh_dimensions()
		
		raw_img = capture_region((
			self.dimensions.center_x - 5, # Left
			self.dimensions.alert_top,    # Top
			self.dimensions.center_x + 5, # Right
			self.dimensions.alert_bottom  # Bottom
		))
		
		return raw_img.convert("L")

	def is_alert_visible(self) -> bool:
		img = self._capture_alert_region()

		_, height = cast(tuple[int, int], img.size)
		pixels = img.load()

		for y in range(height - 1, -1, -5):
			if pixels[0, y] > WHITE_LEVEL: return True
		return False
	
	def await_alert(self):
		print("Waiting for a bite... ", end = "", flush = True)
		sleep(CAST_WAIT)
		
		num_checks = (CAST_WAIT * 2)
		while not self.is_alert_visible():
			sleep(0.5)
			num_checks += 1
			if num_checks >= (CAST_TIMEOUT * 2): break
		print(f"({num_checks/2})")

	def reel_in(self):
		self.activate()
		
		self.center_mouse(0.1)
		for _ in range(CLICK_COUNT):
			ahk.click()
			sleep(0.05)

		print("Hopefully I caught something cool.")

# ── Initialize ────────────────────────────────────────────────────────────── #

def main():
	print("Running Arcane Odyssey auto fisher.\n")
	client = Window()
	client.activate()
	eat_time = perf_counter() + (60 * FOOD_INTERVAL)

	while True:
		ahk.key_press(FISHING_POLE_SLOT)
		
		client.cast_rod()
		client.await_alert()
		client.reel_in()

		if perf_counter() > eat_time:
			eat_time += (60 * FOOD_INTERVAL)
			ahk.key_press(FOOD_SLOT)
			ahk.click()
			sleep(0.25)
		else:
			ahk.key_press(FISHING_POLE_SLOT)
		sleep(0.5)

if __name__ == "__main__":
	try: main()
	except KeyboardInterrupt:
		print("⭕ It's time to go home.")
input("Press any key to close.")