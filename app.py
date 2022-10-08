
# import nest_asyncio
from playwright.async_api import async_playwright
import time
import json
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI
import uvicorn
import subprocess

subprocess.run(["playwright", "install"])
subprocess.run(["playwright", "install-deps"])


async def scrap():
    items = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.ergodotisi.com/en/SearchResults.aspx")

        i = 0
        # while i < 15:
        #     await page.mouse.wheel(0, 4000)
        #     await page.wait_for_timeout(3000)
        #     # page.wait_for_selector("text=More Job Posts...", 3000)
        #     await page.locator("text=More Job Posts...").click()
        #     time.sleep(4)
        #     i = i + 1

        time.sleep(3)
        html = await page.content()

        soup = bs(html, 'html.parser')
        # print(soup.prettify())
        allListing = soup.find_all(
            'article', attrs={'class': 'search-result-card'})
        # print(len(allListing))
        for listing in allListing:
            if ("yesterday" in listing.find_all("p")[3].text):
                # print(listing.find_all("p")[3].text)
                item = {
                    "title": listing.find_all("a")[0].text,
                    "url": listing.find_all("a")[1].text,
                    "city": listing.find_all("p")[0].text,
                    "cmpy": listing.find_all("p")[1].text,
                    "view": listing.find_all("p")[2].text,
                    "date": listing.find_all("p")[3].text,
                    "expire": listing.find_all("p")[4].text,
                    "typeofjob": listing.find_all("p")[5].text
                }
                items.append(item)
        await browser.close()
    return items

app = FastAPI()


@app.get('/')
async def root():
    # items = await scrap()
    data = {"data": "Hello Shiv", "Timestamp": time.time()}
    json_dump = json.dumps(data)
    # print("running server...")
    return json_dump


# if __name__ == '__main__':
#     uvicorn.run("app")


# ngrok_tunnel = ngrok.connect(8000)
# print("Public URL : ", ngrok_tunnel.public_url)
# nest_asyncio.apply()

if __name__ == '__main__':
    uvicorn.run("app")

# if __name__ == '__main__':
#     uvicorn.run("app:app", port=8001, host='127.0.0.2')
