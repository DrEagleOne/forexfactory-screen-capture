# Forex Factory Screen Capture 📈

A simple automation tool to capture daily calendar data from [Forex Factory](https://www.forexfactory.com/calendar) using a real browser to bypass aggressive bot detection.

## How it Works

Since Forex Factory employs strict anti-bot measures, this tool avoids using headless browsers or standard scraping libraries. Instead, it leverages the local system's installed Google Chrome and macOS `screencapture` utility to take a high-fidelity snapshot of the calendar.

## Requirements

- **macOS** (Required for `open`, `screencapture`, and `osascript`).
- **Google Chrome** installed.

## Installation

```bash
git clone https://github.com/DrEagleOne/forexfactory-screen-capture.git
cd forexfactory-screen-capture
```

## Usage

Run the script using Python 3:

```bash
python3 main.py
```

### Options

- `--date`: Specify a date in `mmmdd.yyyy` format (e.g., `apr23.2026`). If omitted, it defaults to today.
- `--output`: Specify the output filename (defaults to `forexfactory.png`).

**Example:**
```bash
python3 main.py --date apr23.2026 --output my_calendar.png
```

## Caution

- **Screen Lock**: Ensure your Mac screen is awake and not locked during the capture process.
- **Resource Management**: The script automatically closes Chrome after capture to prevent memory leaks.
