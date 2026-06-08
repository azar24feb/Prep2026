#!/usr/bin/env python3
"""
replays.py

Usage:
  python replays.py laliga               # fetch FanCode LaLiga replays for default club (real-madrid)
  python replays.py laliga real-madrid  # explicit club
  python replays.py ucl                 # fetch SonyLIV UCL replays for default club (real-madrid)
  python replays.py ucl "real madrid"   # accepts spaces; will normalize to 'real-madrid'

Prints matching replay links to stdout (one per line).
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Default pages
FANCODE_LALIGA_VIDEOS = "https://www.fancode.com/football/tour/spanish-la-liga-season-2025-2026-18801700/video-highlights"
SONYLIV_UCL_LISTING = "https://www.sonyliv.com/listing/full-match-replay-2025-26-1111_9014265?contentId=1700000773"

# timeouts
SHORT_WAIT = 8
LONG_WAIT = 20

def normalize_club(raw: str) -> str:
    """Normalize club name for matching in URLs:
       - trim, lowercase, replace spaces with hyphens
    """
    if not raw:
        return "real-madrid"
    s = raw.strip().lower()
    s = s.replace(" ", "-")
    return s

def start_driver(headless: bool = False):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1600,1000")
    chrome_options.add_argument("--disable-gpu")
    if headless:
        chrome_options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_fancode_replays(driver, club: str, url: str = FANCODE_LALIGA_VIDEOS):
    """
    Fetch replay links from FanCode LaLiga Videos page.
    We look for anchors after the <h2>Replays</h2> whose href contains both club and 'full-replay'.
    """
    wait = WebDriverWait(driver, LONG_WAIT)
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Find Replays <h2> (case-insensitive)
    replays_h2_xpath = "//h2[translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='replays']"
    try:
        replays_h2 = WebDriverWait(driver, SHORT_WAIT).until(
            EC.presence_of_element_located((By.XPATH, replays_h2_xpath))
        )
    except Exception:
        # if Replays heading not found, still try a broad search on the page
        replays_h2 = None

    # Scroll small amount to trigger lazy load of that area (if found)
    if replays_h2 is not None:
        driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", replays_h2)
        time.sleep(0.8)

    # Build XPath to find anchors after Replays heading (or anywhere if heading not found)
    club_esc = club  # already normalized
    xpath_base = (
        "//h2[translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='replays']"
        "/following::a"
    ) if replays_h2 is not None else "//a"

    xpath = (
        xpath_base +
        "[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{club}')"
        " and contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'full-replay')]"
    ).format(club=club_esc)

    # Try presence_of_all_elements_located, but be tolerant to absence
    links = []
    try:
        elems = WebDriverWait(driver, SHORT_WAIT).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
    except Exception:
        elems = []

    # extract unique hrefs preserving order
    seen = set()
    for e in elems:
        href = e.get_attribute("href")
        if href and href not in seen:
            seen.add(href)
            links.append(href)

    # If none found, do a light incremental scroll to load more and retry
    if not links:
        for _ in range(6):
            driver.execute_script("window.scrollBy(0, 700);")
            time.sleep(0.6)
            more = driver.find_elements(By.XPATH, xpath)
            added = False
            for e in more:
                href = e.get_attribute("href")
                if href and href not in seen:
                    seen.add(href)
                    links.append(href)
                    added = True
            if added:
                break

    return links

def fetch_sonyliv_replays(driver, club: str, url: str = SONYLIV_UCL_LISTING):
    """
    Fetch replay links from SonyLIV listing page.
    We'll look for anchors whose href contains the club string and 'replay' (case-insensitive).
    """
    wait = WebDriverWait(driver, LONG_WAIT)
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # small scroll to trigger lazy load on listing
    driver.execute_script("window.scrollBy(0, 600);")
    time.sleep(1.0)

    club_esc = club
    # XPath: find anchors anywhere on page with club and 'replay' in href
    xpath = (
        "//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{club}')"
        " and contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'replay')]"
    ).format(club=club_esc)

    links = []
    seen = set()
    try:
        elems = WebDriverWait(driver, SHORT_WAIT).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
    except Exception:
        elems = []

    for e in elems:
        href = e.get_attribute("href")
        if href:
            # SonyLIV often includes '?watch=true' — keep whatever is present
            if href not in seen:
                seen.add(href)
                links.append(href)

    # If none or partial, do incremental scroll to load more content
    if not links:
        for _ in range(8):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(0.6)
            more = driver.find_elements(By.XPATH, xpath)
            for e in more:
                href = e.get_attribute("href")
                if href and href not in seen:
                    seen.add(href)
                    links.append(href)
            if links:
                break

    return links

def main():
    if len(sys.argv) < 2:
        print("Usage: python replays.py <laliga|ucl> [club-name]")
        sys.exit(1)

    mode = sys.argv[1].strip().lower()
    club_input = sys.argv[2] if len(sys.argv) > 2 else "real-madrid"
    club = normalize_club(club_input)

    # start browser
    driver = start_driver(headless=False)  # change to True to run headless
    try:
        if mode == "laliga":
            results = fetch_fancode_replays(driver, club)
        elif mode == "ucl":
            results = fetch_sonyliv_replays(driver, club)
        else:
            print("Unknown mode. Use 'laliga' or 'ucl'.")
            results = []

        if not results:
            print("No matching replay links found.")
        else:
            for link in results:
                print(link)

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
