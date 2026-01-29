from pyperclip import copy as copy_to_clipboard # install: pyperclip
from dotenv import load_dotenv; load_dotenv()
from os import getenv as get_env
from requests import post
import json

# ── Config ────────────────────────────────────────────────────────────────── #

USER_ID = 998796
KEEP_OPEN = False

# ── Initialize ────────────────────────────────────────────────────────────── #

def main():
	print("\nRequesting current server information...")

	response = post("https://presence.roblox.com/v1/presence/users",
		headers = {
			"Accept":       "application/json",
			"Content-Type": "application/json",
			"Cookie": f".ROBLOSECURITY={get_env('ROBLOX_COOKIE')}" },
		data = json.dumps({"userIds": [USER_ID]})
	)
	assert response.ok, "Failed to get presence"
	
	presence = response.json()["userPresences"][0]
	print(f'It seems like you are playing "{presence["lastLocation"]}"\n')

	command = f"/lock instance place: {presence['placeId']} instance: {presence['gameId']}"
	
	print(command)
	copy_to_clipboard(command)
	print("Copied to clipboard.")

if __name__ == "__main__":
	main()
if KEEP_OPEN:
	input("\nYou can press any key to close.")