from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import json
import pyautogui
import pyperclip
import os


# Set Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Optional: Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Optional: Disable GPU acceleration
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.accept_untrusted_certs = True

# Set ChromeDriver service
service = Service('chromedriver.exe')

# Instantiate the WebDriver with options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Enable the DevTools "Network" domain
driver.execute_cdp_cmd('Network.enable', {})

# Visit the webpage
driver.get('https://ibjjf.com/registered-academies#')

# Set custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://ibjjf.com/registered-academies'
}

# Set the custom headers using Network.setExtraHTTPHeaders
driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})

# Create a list to store the network logs
network_logs = []

def locationViaImage(imagePath, max_attempts=3, confidence=0.8):
    for attempt in range(max_attempts):
        searchingFor = imagePath  # Path to the image of the search icon
        image_location = pyautogui.locateOnScreen(searchingFor, confidence=confidence)
        if image_location:
            print('Found the icon.')
            image_center = pyautogui.center(image_location)
            pyautogui.click(image_center)
            time.sleep(1)  # Allow time for the search icon click to take effect
            return True  # Image found, exit the function
        else:
            print(f'Image not found. Retrying attempt {attempt + 1}/{max_attempts}...')
            time.sleep(1)  # Add a delay between attempts

    print(f'Image not found after {max_attempts} attempts.')
    return False  # Image not found after all attempts



for pageNum in range(1, 358):

    # Disable fail-safe
    pyautogui.FAILSAFE = False

    # Make the screen full size
    pyautogui.press('f11')
    time.sleep(1)  # Allow time for the screen to maximize

    # Simulate pressing F12 to focus on DevTools
    pyautogui.press('f12')
    time.sleep(2)  # Allow time for the focus to change


    

    # Make the screen full size
    pyautogui.press('f11')
    time.sleep(1)  # Allow time for the screen to maximize

    if pageNum==1:
        # find settings dots
        print("Looking for windows settings dots...")
        locationViaImage('windowSettings.png', max_attempts=5, confidence=0.9)

        # find popout into separate window
        print("Looking for popout button...")
        locationViaImage('popOut.png', max_attempts=5, confidence=0.9)

        print("Switching to the Network tab...")
        time.sleep(1)  # Add a delay before switching to the Network tab
        pyautogui.hotkey('ctrl', 'shift', 'p')
        time.sleep(1) 

        # Type "network" to search for the Network tab
        pyautogui.typewrite('network')
        
        time.sleep(1)  # Allow time for the Network tab to load
        print("Switched to the Network tab.")

        # Continue with your code for interacting with the Network tab

        # Press Enter to confirm the search and load the Network tab
        pyautogui.press('enter')
        time.sleep(1)  # Allow time for the search to update

        # refresh the logs
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(1)

        # find preserve log checkbox
        print("Looking for preserve log checkbox...")
        locationViaImage('preserveLog.png', max_attempts=5, confidence=0.9)

        

        




    # Perform image recognition and click on the search icon
    locationViaImage('searchIcon.png', max_attempts=5, confidence=0.9)


    pyautogui.typewrite(f'list.json?page={pageNum}')
    time.sleep(1)  # Allow time for the text to be typed
    pyautogui.press('enter')
    time.sleep(1)  # Allow time for the response tab to load

    # Navigate to the first result
    pyautogui.press('tab', presses=3)
    time.sleep(0.5)  # Add a small delay before pressing down
    pyautogui.press('down')
    time.sleep(0.5)  # Add a small delay before pressing enter
    pyautogui.press('enter')
    time.sleep(1)  # Allow time for the response tab to load

    # Perform image recognition and click on the Response tab

    locationViaImage('responseTab.png', max_attempts=5, confidence=0.9)


    # Enter response body
    pyautogui.press('enter')
    time.sleep(1)  # Allow time for the response body to load
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)  # Add a small delay before copying
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Add a small delay after copying

    # Retrieve the text from the clipboard
    clipboard_text = pyperclip.paste()

    # Specify the file path and name
    file_path = f'data/academyData_page{pageNum}.json'

    # Write the clipboard text to the file
    with open(file_path, 'w') as file:
        file.write(clipboard_text)

    # close dev tools
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)  # Allow time for the Network tab to load



     # Check if the file exists
    if os.path.isfile(file_path):

        
        # Pagination process
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'next-page'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        time.sleep(5)
    else:
        print(f"Failed to write file for page {pageNum}.")


    

    time.sleep(500)



    # # clicks on next page (list.json?page=2)
    # element = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, 'next-page'))
    # )
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    # element.click()
    # time.sleep(5)



# Quit the WebDriver
driver.quit()


