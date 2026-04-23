import subprocess
import time
import sys
import argparse
import os
from datetime import datetime

# Optimized crop for 2560x1440 screen to keep only the central calendar content
# X=630, Y=160, Width=1300, Height=1000
DEFAULT_CROP = "630,160,1300,1000"

def capture_forex_factory(date_str=None, output_path="forexfactory.png", crop=None):
    """
    Captures a screenshot of the Forex Factory calendar for a specific date.
    
    Args:
        date_str (str): Date in format 'mmmdd.yyyy' (e.g., 'apr23.2026'). 
                        If None, today's date is used.
        output_path (str): Path to save the resulting screenshot.
        crop (str): Crop rectangle in 'x,y,w,h' format.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%b%d.%Y").lower()
    
    # Convert relative path to absolute path
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    
    url = f"https://www.forexfactory.com/calendar?day={date_str}"
    
    try:
        print(f"[*] Opening URL in Google Chrome: {url}")
        subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        
        # Increased wait time to 25s to ensure Cloudflare is bypassed and page is loaded
        wait_time = 25 
        print(f"[*] Waiting {wait_time} seconds for Cloudflare and page to fully load...")
        time.sleep(wait_time)
        
        print(f"[*] Capturing screen to {output_path}...")
        if crop:
            print(f"[*] Capturing cropped screen ({crop})...")
            subprocess.run(["screencapture", "-D", "1", "-xC", "-R", crop, output_path], check=True)
        else:
            print(f"[*] Capturing full screen...")
            subprocess.run(["screencapture", "-D", "1", "-xC", output_path], check=True)
        
        print("[*] Closing Google Chrome to save resources...")
        subprocess.run(["osascript", "-e", 'quit app "Google Chrome"'], check=True)
        
        print(f"[+] Success! Screenshot saved to: {output_path}")
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
    parser.add_argument("--crop", type=str, default=DEFAULT_CROP, help="Crop rectangle 'x,y,w,h'. Defaults to standard crop.")
    parser.add_argument("--full", action="store_true", help="Capture full screen instead of cropping.")
    
    args = parser.parse_args()
    
    crop_val = None if args.full else args.crop
    capture_forex_factory(args.date, args.output, crop_val)
