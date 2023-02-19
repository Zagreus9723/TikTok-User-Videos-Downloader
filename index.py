import asyncio
import io
import glob
import os
import time
import urllib.request
from os import path
import aiohttp
from tiktokapipy.async_api import AsyncTikTokAPI
from tiktokapipy.models.video import Video
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

async def download_video():
    # mobile emulation is necessary to retrieve slideshows
    # if you don't want this, you can set emulate_mobile=False and skip if the video has an image_post property
    async with AsyncTikTokAPI(emulate_mobile=True) as api:
        if not os.path.exists(f'videos\\{user_tag}'):
            os.mkdir(f'videos\\{user_tag}')
        user = await api.user(user_tag)
        async for vid in user.videos:
            print(vid.id)
            options = webdriver.ChromeOptions()
            options.add_extension("ad.crx")
            prefs = {"download.default_directory": f"{sys.argv[0].replace('index.py', '')}videos\\{user_tag}"}
            options.add_experimental_option("prefs", prefs)
            browser = webdriver.Chrome(options=options)
            time.sleep(8)
            browser.get('https://snaptik.app')
            x = browser.find_element(By.XPATH, "/html/body/main/div[1]/div/div[2]/form/div/div[3]/input")
            x.send_keys(f'https://www.tiktok.com/@{user_tag}/video/{vid.id}?lan=en')
            but = browser.find_element(By.XPATH, "/html/body/main/div[1]/div/div[2]/form/div/div[4]/button")
            but.click()
            downloaded = False
            while not downloaded:
                try:
                    download = browser.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div[2]/div/a[1]")
                    download.click()
                    time.sleep(2)
                    saved = False
                    while not saved:
                        if os.path.exists(f"videos\\{user_tag}\\Snaptik.app_{vid.id}.mp4"):
                            saved = True
                            browser.quit()
                        else:
                            time.sleep(1)
                    downloaded = True
                except:
                    time.sleep(5)

user_tag = input("What user\n[?]: ")
asyncio.run(download_video())