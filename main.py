import subprocess
import time
import sys
import argparse
from datetime import datetime

def capture_forex_factory(date_str=None, output_path="forexfactory.png"):
    """
    Captures a screenshot of the Forex Factory calendar for a specific date.
    
    Args:
        date_str (str): Date in format 'mmmdd.yyyy' (e.g., 'apr23.2026'). 
                        If None, today's date is used.
        output_path (str): Path to save the resulting screenshot.
    """
    if date_str is None:
        # Default to today's date in mmmdd.yyyy format
        date_str = datetime.now().strftime("%b%d.%Y").lower()
    
    url = f"https://www.forexfactory.com/calendar?day={date_str}"
    
    try:
        print(f"[*] Opening URL in Google Chrome: {url}")
        subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        
        print("[*] Waiting 10 seconds for the page to fully load...")
        time.sleep(10)
        
        print(f"[*] Capturing screen to {output_path}...")
        subprocess.run(["screencapture", "-x", output_path], check=True)
        
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
    
    args = parser.parse_args()
    capture_forex_factory(args.date, args.output)
