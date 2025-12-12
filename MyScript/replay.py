#!/usr/bin/env python3
"""
replay.py

Usage:
  python replay.py               # laliga mode, default club real-madrid
  python replay.py laliga        # explicit laliga
  python replay.py ucl           # sonyLiv (ucl) mode, default club real-madrid
  python replay.py ucl "manchester city"  # club name (spaces allowed)

Prints matching replay links (one per line). If none found prints:
  No matching replay links found.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# URLs
FANCODE_LALIGA_VIDEOS = "https://www.fancode.com/football/tour/spanish-la-liga-season-2025-2026-18801700/video-highlights"
SONYLIV_UCL_LISTING = "https://www.sonyliv.com/listing/full-match-replay-2025-26-1111_9014265?contentId=1700000773"
MODE = "ucl"

# small helpers
def normalize_club(raw: str) -> str:
    if not raw:
        return "real-madrid"
    s = raw.strip().lower()
    s = s.replace(" ", "-")
    return s

def start_driver(headless: bool = False):
    opts = Options()
    opts.add_argument("--window-size=1600,1000")
    opts.add_argument("--disable-gpu")
    if headless:
        opts.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver

def fetch_fancode(driver, club_normalized):
    """
    Find anchors after the Replays <h2> whose href contains both club_normalized and 'full-replay'
    Uses light polling and limited scroll attempts to avoid hanging.
    """
    driver.get(FANCODE_LALIGA_VIDEOS)
    # Wait a little for page to load
    time.sleep(1.2)

    # Try to find the Replays H2 (case-insensitive)
    try:
        replays_h2 = driver.find_elements(By.XPATH,
            "//h2[translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='replays']")
        if replays_h2:
            # scroll into view first Replays header found
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", replays_h2[0])
            except Exception:
                pass
            time.sleep(0.8)
    except Exception:
        pass

    # xpath to search anchors AFTER the Replays heading if present, otherwise search all anchors
    xpath_after_replays = ("//h2[translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='replays']"
                           "/following::a")
    xpath_all_anchors = "//a"

    # use the 'href contains both' filter appended
    club = club_normalized
    filter_tail = ("[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{club}')"
                   " and contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'full-replay')]").format(club=club)

    # prefer scoped search (after replays), fallback to global if replays not found
    use_xpath = xpath_after_replays + filter_tail
    # We will attempt a small number of passes to allow lazy-loading
    found_links = []
    seen = set()

    for attempt in range(6):
        try:
            elems = driver.find_elements(By.XPATH, use_xpath)
        except Exception:
            elems = []

        # collect unique hrefs
        for e in elems:
            try:
                href = e.get_attribute("href")
                if href and href not in seen:
                    seen.add(href)
                    found_links.append(href)
            except Exception:
                pass

        if found_links:
            break

        # if nothing found and on first attempts, try fallback global xpath (maybe header not present)
        if attempt == 2 and not found_links:
            use_xpath = xpath_all_anchors + filter_tail

        # light scroll to load more content before next attempt
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(0.7)

    return found_links

def fetch_sonyliv(driver, club_normalized):
    """
    Find anchors whose href contains club_normalized and 'replay' on the SonyLIV listing.
    Uses limited polling and incremental scrolling to avoid getting stuck.
    """
    driver.get(SONYLIV_UCL_LISTING)
    time.sleep(1.0)

    # initial light scroll to trigger lazy content
    try:
        driver.execute_script("window.scrollBy(0, 600);")
    except Exception:
        pass
    time.sleep(0.9)

    club = club_normalized
    xpath = ("//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{club}')"
             " and contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'replay')]").format(club=club)

    found_links = []
    seen = set()

    # do several attempts with scrolls
    for attempt in range(10):
        try:
            elems = driver.find_elements(By.XPATH, xpath)
        except Exception:
            elems = []

        for e in elems:
            try:
                href = e.get_attribute("href")
                if href and href not in seen:
                    seen.add(href)
                    found_links.append(href)
            except Exception:
                pass

        if found_links:
            break

        # incremental scroll and small wait
        try:
            driver.execute_script("window.scrollBy(0, 800);")
        except Exception:
            pass
        time.sleep(0.6)

    return found_links

def main():
    # defaults: mode = laliga, club = real-madrid
    if len(sys.argv) == 1:
        mode = MODE
        club_input = "real-madrid"
    else:
        mode = sys.argv[1].strip().lower()
        print(mode)
        club_input = sys.argv[2] if len(sys.argv) > 2 else "real-madrid"

    if mode not in ("laliga", "ucl"):
        print("Invalid Input, try python replay.py laliga/ucl")  # keep output minimal if invalid mode
        return
    #     # treat single-arg that isn't recognized as mode as club name, keep laliga
    #     if len(sys.argv) == 2:
    #         mode = "laliga"
    #         club_input = sys.argv[1]
    #     else:
    #         print("No matching replay links found.")  # keep output minimal if invalid mode
    #         return

    club_norm = normalize_club(club_input)

    driver = start_driver(headless=True)  # set True if you want headless
    try:
        if mode == "laliga":
            results = fetch_fancode(driver, club_norm)
        else:  # mode == "ucl"
            results = fetch_sonyliv(driver, club_norm)

        if not results:
            print("No matching replay links found.")
        else:
            for r in results:
                print(r)

    except Exception:
        # Ensure we print minimal output on unexpected exception
        print("No matching replay links found.")
    finally:
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
