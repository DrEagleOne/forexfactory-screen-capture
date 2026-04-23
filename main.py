import subprocess
import time
import sys
import argparse
import os
from datetime import datetime
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
    HAS_CROP_DEPS = True
except ImportError:
    HAS_CROP_DEPS = False

# Default manual crop for 2560x1440 screen
DEFAULT_CROP = "630,160,1300,1000"

def auto_crop_image(input_path):
    """
    Automatically crops the image to remove sidebars and browser UI.
    Based on pixel brightness analysis.
    """
    if not HAS_CROP_DEPS:
        print("[-] Auto-crop dependencies (numpy, Pillow) not installed.")
        return None

    img = Image.open(input_path).convert("RGB")
    arr = np.array(img)
    w, h = img.size

    # 1. Left/Right Bounds: Find the transition from dark background to browser
    col_b = arr.mean(axis=(0, 2))
    
    def find_left_bound(col_b, dark=80, run=10):
        count = 0
        for i, b in enumerate(col_b):
            if b < dark:
                count += 1
            else:
                if count >= run: return i
                count = 0
        return 0

    def find_right_bound(col_b, dark=80, run=10):
        count = 0
        for i in range(len(col_b)-1, -1, -1):
            if col_b[i] < dark:
                count += 1
            else:
                if count >= run: return i + 1
                count = 0
        return len(col_b)

    left = find_left_bound(col_b)
    right = find_right_bound(col_b)

    # 2. Top/Bottom Bounds: Use right half to detect white table
    half = left + (right - left) // 2
    rb = arr[:, half:right, :].mean(axis=(1, 2))

    top = 0
    for i in range(len(rb) - 5):
        if all(rb[i:i+5] > 210):
            top = i
            break

    bottom = len(rb)
    for i in range(top, len(rb) - 20):
        if all(rb[i:i+20] < 210):
            bottom = i
            break

    cropped = img.crop((left, top, right, bottom))
    cropped.save(input_path, quality=95)
    print(f"[*] Auto-cropped: left={left}, top={top}, right={right}, bottom={bottom}")
    return input_path

def capture_forex_factory(date_str=None, output_path="forexfactory.png", crop=None, auto_crop=False):
    if date_str is None:
        date_str = datetime.now().strftime("%b%d.%Y").lower()
    
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    
    url = f"https://www.forexfactory.com/calendar?day={date_str}"
    
    try:
        print(f"[*] Opening URL in Google Chrome: {url}")
        subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        
        wait_time = 25 
        print(f"[*] Waiting {wait_time} seconds for Cloudflare and page to fully load...")
        time.sleep(wait_time)
        
        if crop:
            print(f"[*] Capturing cropped screen ({crop}) to {output_path}...")
            subprocess.run(["screencapture", "-D", "1", "-x", "-R", crop, output_path], check=True)
        else:
            print(f"[*] Capturing full screen to {output_path}...")
            subprocess.run(["screencapture", "-D", "1", "-x", output_path], check=True)
        
        if auto_crop:
            print("[*] Applying automatic border cropping...")
            auto_crop_image(output_path)
        
        print("[*] Closing Google Chrome to save resources...")
        subprocess.run(["osascript", "-e", 'quit app "Google Chrome"'], check=True)
        
        print(f"[+] Success! Final image saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Error occurred: {e}")
        return False
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture Forex Factory Calendar screenshots.")
    parser.add_argument("--date", type=str, help="Date in mmmdd.yyyy format (e.g., apr23.2026). Defaults to today.")
    parser.add_argument("--output", type=str, default="forexfactory.png", help="Output filename for the screenshot.")
    parser.add_argument("--crop", type=str, default=DEFAULT_CROP, help="Crop rectangle 'x,y,w,h'.")
    parser.add_argument("--full", action="store_true", help="Capture full screen (no crop).")
    parser.add_argument("--auto-crop", action="store_true", help="Automatically crop borders based on pixel brightness.")
    
    args = parser.parse_args()
    
    crop_val = None if args.full else args.crop
    capture_forex_factory(args.date, args.output, crop_val, args.auto_crop)
