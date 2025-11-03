from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore, Style
from time import sleep

import InputFunctions as IF
import MiscFunctions
import EssentialFunctions


def get_user_configuration():
    """
    Gathers all necessary inputs from the user and returns them in a settings dictionary.
    """
    print(f"{Style.BRIGHT}--- Google Image Scraper Utility ---{Style.RESET_ALL}")
    print("NOTE: Make sure you have the latest version of Google Chrome installed.")
    print("Enter the URL of a Google Images search result page (e.g., https://www.google.com/search?q=sample&tbm=isch)")

    target_url = IF.takeInput("Enter URL to scrape")

    print("\nRecommended time delay between clicks is 1-2 seconds (longer delay is safer).")
    time_delay = IF.takeInputFloat("Enter Time Delay")

    print("\nBe careful: too high a value may block your IP.")
    print("Set to 0 if you want to bulk download from an existing .bin file.")
    image_count = IF.takeInputInt("Enter Amount of Images to Scrape")

    output_dir = None
    if IF.takeInputYesNo("\nSave Images to Directory?"):
        output_dir = IF.takeInput("Enter Folder Name for Output")
        MiscFunctions.createFolder(output_dir)  # Create folder if specified

    bin_filename = IF.takeInput("Enter filename for scraped URLs (do not add .bin)")

    # Return all settings as a single dictionary
    return {
        "url": target_url,
        "delay": time_delay,
        "amount": image_count,
        "directory": output_dir,
        "filename": bin_filename,
    }


def run_scrape_task(config):
    """
    Executes the main scraping or downloading logic based on the user's configuration.
    """
    print(f"{Fore.BLUE}\nProgram will slow down near the end due to duplicate image filtering.")
    sleep(2)

    # For Scrape new images
    if config["amount"] > 0:
        print(f"{Fore.GREEN}Initializing WebDriver to scrape {config['amount']} images...")
        driver = None
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.maximize_window()
            EssentialFunctions.scrapGoogleImagesURLs(
                config["url"],
                driver,
                config["delay"],
                config["amount"],
                config["directory"],
                config["filename"]
            )
            print(f"{Fore.GREEN}Scraping task completed successfully.")
        except Exception as e:
            print(f"{Fore.RED}An error occurred during scraping: {e}")
        finally:
            if driver:
                driver.quit()
                print(f"{Fore.CYAN}WebDriver closed.")

    # Bulk download from existing file
    elif config["amount"] == 0:
        output_folder = config["directory"] or "NoNameProvided"
        print(f"{Fore.BLUE}Starting bulk download from '{config['filename']}.bin' to '{output_folder}'...")
        try:
            EssentialFunctions.BulkDownload(config["filename"], output_folder)
            print(f"{Fore.GREEN}Bulk download complete.")
        except Exception as e:
            print(f"{Fore.RED}An error occurred during bulk download: {e}")


def main():
    """
    Main entry point for the script.
    """
    init(autoreset=True)

    MiscFunctions.createFolder("Bin Files", False)

    try:
        settings = get_user_configuration()

        run_scrape_task(settings)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user. Exiting.")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {e}")
    finally:
        print(f"\n{Style.DIM}Program finished.")


if __name__ == "__main__":
    main()
