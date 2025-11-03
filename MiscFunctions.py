import os
import time
import pickle
import hashlib
from selenium.webdriver.common.by import By
from colorama import Fore

# ------------------------------
# Constants
# ------------------------------
MAX_RETRIES = 5
CURRENT_TRIALS = 0
SHOW_MORE_CLASSES = ["LZ4I", "XfJHbe", "mye4qd"]  # Add more if Google changes layout


# ------------------------------
# Folder and File Utilities
# ------------------------------
def createFolder(folderName, showConfirmation=False):
    folderDirectory = getFilePath(folderName)
    try:
        os.makedirs(folderDirectory, exist_ok=True)
        if showConfirmation:
            print(f"{Fore.GREEN}Created folder {folderName} at {folderDirectory}")
    except Exception as e:
        if showConfirmation:
            print(f"{Fore.YELLOW}Folder creation failed: {e}")


def getFilePath(*filesAndFolders):
    return os.path.join(os.getcwd(), *filesAndFolders)


# ------------------------------
# Scrolling and Clicking
# ------------------------------
def scrollDown(WEB_DRIVER, scrolls=6, delay=2):
    last_height = WEB_DRIVER.execute_script("return document.body.scrollHeight")
    for _ in range(scrolls):
        WEB_DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = WEB_DRIVER.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def clickWebElement(WEB_DRIVER, webElement):
    try:
        WEB_DRIVER.execute_script("arguments[0].scrollIntoView();", webElement)
        WEB_DRIVER.execute_script("arguments[0].click();", webElement)
        time.sleep(1)
    except Exception as e:
        print(f"{Fore.YELLOW}Failed to click element: {e}")


def getWebElementsToClick(WEB_DRIVER):
    elements = []
    for className in SHOW_MORE_CLASSES:
        elements += WEB_DRIVER.find_elements(By.CLASS_NAME, className)
    return elements


def reachBottomOfPage(WEB_DRIVER):
    scrollDown(WEB_DRIVER)
    print(f"{Fore.BLUE}Preparatory pass done")

    for elm in getWebElementsToClick(WEB_DRIVER):
        clickWebElement(WEB_DRIVER, elm)

    scrollDown(WEB_DRIVER)
    print(f"{Fore.BLUE}First pass done")

    for elm in getWebElementsToClick(WEB_DRIVER):
        clickWebElement(WEB_DRIVER, elm)

    scrollDown(WEB_DRIVER)
    print(f"{Fore.BLUE}Final pass done")
    WEB_DRIVER.execute_script("window.scrollTo(0,0);")


# ------------------------------
# Pickle Utilities
# ------------------------------
def loadPickledFile(fileName):
    filePath = getFilePath("Bin Files", fileName + ".bin")
    try:
        with open(filePath, "rb") as f:
            return pickle.load(f)
    except:
        print(f"{Fore.YELLOW}File {fileName}.bin does not exist or could not be read")
        return set()


def savePickleFile(fileName, data):
    if not data:
        print(f"{Fore.YELLOW}No data to save. {fileName}.bin won't be saved.")
        return
    filePath = getFilePath("Bin Files", fileName + ".bin")
    try:
        with open(filePath, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"{Fore.RED}Failed to save {fileName}.bin: {e}")


# ------------------------------
# Helpers
# ------------------------------
def shortenString(inputString, finalLength=16):
    hashedString = hashlib.sha256(str(inputString).encode()).hexdigest()
    return hashedString[:finalLength]
