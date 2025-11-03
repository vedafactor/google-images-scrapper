import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By
from MiscFunctions import *
import time
from colorama import Fore
import os

TIME_OUT = 5

# ------------------------------
# Helper function to download images
# ------------------------------
def downloadImage(url, fileName, downloadPath=getFilePath("ImagesOutput")):
    try:
        os.makedirs(downloadPath, exist_ok=True)
    except:
        pass

    if os.path.exists(getFilePath(downloadPath, fileName)):
        print(f"{Fore.YELLOW}The image {fileName} already exists")
        return
    if fileName is None:
        print(Fore.RED + "ERROR: filename cannot be empty")
        return

    try:
        imageContent = requests.get(url, timeout=TIME_OUT).content
        try:
            imageFile = io.BytesIO(imageContent)
            finalImage = Image.open(imageFile)
            if finalImage.mode != "RGB":
                finalImage = finalImage.convert("RGB")
        except Exception as e:
            print(f"{Fore.RED}Failed to open/convert {url}: {e}")
            return

        extension = ".jpg"
        if ".png" in url:
            extension = ".png"
        elif ".gif" in url:
            extension = ".gif"
        elif ".webp" in url:
            extension = ".webp"
        elif ".svg" in url:
            extension = ".svg"

        imagePath = getFilePath(downloadPath, fileName + extension)

        if extension != ".svg":
            with open(imagePath, "wb") as f:
                finalImage.save(f)
                finalImage.close()
        else:
            with open(imagePath, "wb") as f:
                f.write(imageContent)

        print(f"{Fore.GREEN}Downloaded {fileName}{extension}")
    except Exception as e:
        print(f"{Fore.RED}Failed to download {fileName} from {url}. Exception: {e}")

# ------------------------------
# Scrape Google Images URLs This is the main block(should be updated based on the changes in google images)
# ------------------------------
def scrapGoogleImagesURLs(SCRAPE_URL, WEB_DRIVER, timeDelay, imageCount, scrapeFolder, scrapeFileName):
    try:
        WEB_DRIVER.get(SCRAPE_URL)
        print(f"{Fore.CYAN}🔍 Loaded URL: {SCRAPE_URL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to load URL: {e}")
        return

    imageURLs = set()
    previousURLs = set()

    # Load previously saved URLs
    if scrapeFileName:
        previousURLs = loadPickledFile(getFilePath("Bin Files", scrapeFileName))
    print(f"{Fore.GREEN}Previously stored URLs: {len(previousURLs)}")

    scroll_pause_time = timeDelay
    current_image_count = 0
    last_height = WEB_DRIVER.execute_script("return document.body.scrollHeight")

    # Main scraping loop
    while len(imageURLs) + len(previousURLs) < imageCount:
        # Broad selector to handle Google's changing DOM
        thumbnails = WEB_DRIVER.find_elements(
            By.CSS_SELECTOR, "img.Q4LuWd, img.YQ4gaf, img.rg_i, img.iPVvYb"
        )
        print(f"{Fore.CYAN}🖼 Found {len(thumbnails)} thumbnail elements...")

        for thumbnail in thumbnails[current_image_count:]:
            try:
                WEB_DRIVER.execute_script("arguments[0].scrollIntoView();", thumbnail)
                thumbnail.click()
                time.sleep(scroll_pause_time + 1.5)  
            except Exception:
                continue

            images = WEB_DRIVER.find_elements(
                By.CSS_SELECTOR, "img.n3VNCb, img.sFlh5c, img.r48jcc, img.iPVvYb, img.YQ4gaf"
            )
            for image in images:
                src = (
                    image.get_attribute("src")
                    or image.get_attribute("data-iurl")
                    or image.get_attribute("data-src")
                )
                if not src or not src.startswith("http"):
                    continue

                if "encrypted-tbn0.gstatic.com" in src and "=s" in src:
                    continue

                if src in imageURLs or src in previousURLs:
                    continue
                if any(ext in src for ext in [".svg", ".gif"]):
                    continue

                imageURLs.add(src)
                current_image_count += 1
                print(f"{Fore.GREEN}✅ Found HD image {current_image_count}: {src[:100]}")

                if len(imageURLs) + len(previousURLs) >= imageCount:
                    break

            if len(imageURLs) + len(previousURLs) >= imageCount:
                break

        WEB_DRIVER.execute_script("window.scrollBy(0, 4000);")
        time.sleep(scroll_pause_time + 2)
        new_height = WEB_DRIVER.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f"{Fore.BLUE}📜 Reached bottom of page.")
            break
        last_height = new_height

    mergedSet = imageURLs.union(previousURLs)
    if mergedSet:
        savePickleFile(getFilePath("Bin Files", scrapeFileName), mergedSet)
        print(f"{Fore.GREEN}💾 Saved {len(mergedSet)} HD image URLs to {scrapeFileName}.bin")
    else:
        print(f"{Fore.YELLOW}⚠️ No new HD images found. Nothing saved.")

    if scrapeFolder:
        print(f"{Fore.GREEN}⬇️ Downloading {len(mergedSet)} HD images to {scrapeFolder}...")
        for url in mergedSet:
            downloadImage(url, shortenString(url, 16), scrapeFolder)
    else:
        print(f"{Fore.GREEN}📁 Scraped {len(mergedSet)} HD image URLs saved to {scrapeFileName}.bin")

    print(f"{Fore.MAGENTA}✨ Scraping completed successfully!")



# ------------------------------
# Bulk download from .bin file
# ------------------------------
def BulkDownload(binFileName, folderName):
    URLSet = loadPickledFile(getFilePath("Bin Files", binFileName))
    if not URLSet:
        print(f"{Fore.RED}Bin file is empty or missing!")
        return
    print(f"{Fore.GREEN}Downloading {len(URLSet)} images to {folderName}...")
    for url in URLSet:
        downloadImage(url, shortenString(url, 16), folderName)
