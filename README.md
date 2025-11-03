<div align="center">
  
  <h1>🖼️ Google Images HD Scraper 🖼️</h1>
  
  <p>
    A robust Python tool to scrape high-resolution images from Google Images using Selenium.
  </p>
  <p>
    It intelligently skips duplicates, filters for high-quality results, and supports bulk downloading from previously scraped URL lists.
  </p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+">
    <img src="https://img.shields.io/badge/Platform-Windows-blue.svg" alt="Windows">
    <img src="https://img.shields.io/badge/Maintained-Yes-green.svg" alt="Maintained">
    <img src="https://img.shields.io/badge/License-open-green.svg" alt="License">
  </p>
  
  <br>

  <img src="[YOUR_DEMO_GIF_HERE].gif" alt="Scraper Demo GIF">

</div>

---

## ✨ Features

* 🧠 **Smart Memory:** Remembers previously scraped URLs (via `.bin` files) to avoid duplicate downloads across sessions.
* 📸 **True HD Quality:** Scrapes the *full, high-resolution* image, not the low-quality thumbnail.
* 📂 **Bulk Downloader:** Option to download all images from a pre-scraped `.bin` file at any time.
* 💾 **Automatic File Handling:** Automatically creates output folders and `.bin` files to store URL sets.
* ⚙️ **Adjustable Delay:** Set a custom time delay between actions to fine-tune performance and avoid rate-limiting.
* 🔄 **Always Up-to-Date:** Uses `webdriver-manager` to automatically download and manage the correct `chromedriver` for your version of Chrome.

---

## ⚠️ Disclaimer & Responsible Use

> **Warning:** This tool is intended for personal and educational use only.
>
> Web scraping, especially from a service like Google, may be against their **Terms of Service (ToS)**. Excessive scraping or automated activity can lead to your IP address being temporarily or permanently blocked by Google.
>
> The developers of this tool are not responsible for any misuse or consequences that arise from using this script. **Use responsibly and at your own risk.**

---

## 🛠️ Requirements & Setup

> ⚠️ **Note:** This tool is designed for **Windows** and requires **Google Chrome** to be installed.

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/YourUsername/Your-Repo-Name.git](https://github.com/vedafactor/google-images-scrapper.git)
    cd google-images-scrapper
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv myenv
    myenv\Scripts\activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    > **No `requirements.txt`?** Install manually:
    > ```bash
    > pip install selenium webdriver-manager colorama
    > ```

4.  **That's it!** You **do not** need to manually download `chromedriver.exe`. The script handles it automatically.

---

## 💻 How to Use

Run the main script from your terminal:
```bash
python main.py
