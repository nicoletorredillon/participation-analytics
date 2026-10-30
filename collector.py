from PIL import ImageGrab
import time
import os

day = input("Which day are we capturing? ")

folder = f"captures/{day}"
os.makedirs(folder, exist_ok=True)

print("Snake Cam starts in 5 seconds...")
time.sleep(5)

for i in range(26):
    screenshot = ImageGrab.grab(bbox=(690, 95, 1280, 760))
    screenshot.save(f"{folder}/capture_{i:02}.png")
    print(f"Captured {i + 1}")
    time.sleep(2)

print("Snake Cam finished!")