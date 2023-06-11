import os
import time
import asyncio

from datetime import datetime
from bs4 import BeautifulSoup

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

actual_year = datetime.now().year
SEASONS =list(range(actual_year - 7, actual_year + 1))

DATA_DIR = 'data'
STANDINGS_DIR = os.path.join(DATA_DIR, 'standings')
SCORES_DIR = os.path.join(DATA_DIR, 'scores')

async def get_html(url, selector, sleep = 1, retries = 5):
    '''
    Asynchronously retrieves the HTML content of a web page using Playwright.
    It opens a browser, navigates to the specified URL, and returns the HTML content
    within the specified selector. It includes optional parameters for sleep time and
    retry attempts in case of timeouts.
    '''
    html = None
    for i in range(1, retries + 1):
        time.sleep(sleep * i)

        try:
            async with async_playwright() as p:
                browser = await p.firefox.launch()
                page = await browser.new_page()
                await page.goto(url)
                print(await page.title())
                html = await page.inner_html(selector)
        
        except PlaywrightTimeout:
            print(f"Timeout error on {url}")
            continue

        else:
            break
    
    return html

async def scrape_season(season):
    '''
    Asynchronously scrapes the standings pages for a specific NBA season.
    It generates the URL for the season's games page, retrieves the HTML content
    using the get_html function, extracts the links from the page, and saves the
    standings pages locally. The function ensures not to overwrite existing files.
    '''
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"
    html = await get_html(url, "#content .filter")

    soup = BeautifulSoup(html, features="html.parser")
    links = soup.find_all("a")
    href = [l["href"] for l in links]
    standings_pages = [f"https://www.basketball-reference.com/{l}" for l in href]

    for url in standings_pages:
        save_path = os.path.join(STANDINGS_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = await get_html(url, "#all_schedule")
        with open(save_path, "w+") as f:
            f.write(html)

def monthly_schedule_html():
    '''
    Scrapes the monthly schedule HTML for each season in the SEASONS list.
    It iterates over each season, calling the `scrape_season` function to scrape
    and save the standings pages for that season. The function executes asynchronously
    using asyncio to allow concurrent scraping for multiple seasons.
    '''
    for season in SEASONS:
        async def main(season):
            await scrape_season(season)
        asyncio.run(main(season))

monthly_schedule_html()

standings_files = os.listdir(STANDINGS_DIR)
standings_files = [s for s in standings_files if ".html" in s]

async def scrape_game(standings_file):
    '''
    Asynchronously scrapes the box scores for each game in a standings file.
    It reads the HTML content from the standings file, extracts the box score links,
    generates the full URLs, and saves the box score HTML locally. The function ensures
    not to overwrite existing files and skips invalid or missing HTML content.
    '''
    with open(standings_file, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, features="html.parser")
    links = soup.find_all("a")
    hrefs = [l.get("href") for l in links]
    box_scores = [l for l in hrefs if l and "boxscore" in l and ".html" in l]
    box_scores = [f"https://www.basketball-reference.com{l}" for l in box_scores]

    for url in box_scores:
        save_path = os.path.join(SCORES_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = await get_html(url, "#content")
        if not html:
            continue
        with open(save_path, "w+") as f:
            f.write(html)

def games_boxscores_html():
    '''
    Scrapes the box scores HTML for each game in the standings files.
    It iterates over each standings file, calling the `scrape_game` function
    to scrape and save the box scores for each game in that file. The function
    executes asynchronously using asyncio to allow concurrent scraping for multiple files.
    '''
    for f in standings_files:
        file_path = os.path.join(STANDINGS_DIR, f)

        async def main(file_path):
            await scrape_game(file_path)
        asyncio.run(main(file_path))

games_boxscores_html()