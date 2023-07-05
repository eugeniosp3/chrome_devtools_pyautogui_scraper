# 'https://ibjjf.com/registered-academies#'
import pyautogui as pag
import time
import pyperclip
import pyscreeze
import PIL

# dependent on pip install opencv-python

# __PIL_TUPLE_VERSION = tuple(int(x) for x in PIL.__version__.split("."))
# pyscreeze.PIL__version__ = __PIL_TUPLE_VERSION



def locationViaImage(imagePath, max_attempts=3, confidence=0.8):
    for attempt in range(max_attempts):
        searchingFor = imagePath  # Path to the image of the search icon
        image_location = pag.locateOnScreen(
            searchingFor, confidence=confidence)
        if image_location:
            print('Found the icon.')
            image_center = pag.center(image_location)
            pag.click(image_center)
            # Allow time for the search icon click to take effect
            time.sleep(1)
            return True  # Image found, exit the function
        else:
            print(
                f'Image not found. Retrying attempt {attempt + 1}/{max_attempts}...')
            time.sleep(1)  # Add a delay between attempts

    print(f'Image not found after {max_attempts} attempts.')
    return False  # Image not found after all attempts



for pageNumber in range(1, 359):
    page = f"list.json?page={pageNumber}"

    time.sleep(3)
    print("Switch Now")
    # just clicks onto the browser from vscode

    # goes to bottom of page
    pag.hotkey('ctrl', 'end')



    # find the search icon and click it
    print("Looking for search icon")
    locationViaImage('searchIcon.png', max_attempts=3, confidence=.95)
    print("Found search icon")

    # paste the string we're searching for into the search bar
    print("Typing into search bar")
    pag.typewrite(page)
    time.sleep(1)
    print("Hit enter to solidify search")
    pag.press('enter')
    time.sleep(1)

    # hits tab 3 times
    print("Hitting tab 3 times and then down and enter")
    pag.press('tab', presses=3)
    time.sleep(1)
    pag.press('down')
    time.sleep(1)
    pag.press('enter')
    time.sleep(1)

    # finds the response tab
    print("Looking for response tab")
    locationViaImage('responseTab.png', max_attempts=3, confidence=0.8)
    time.sleep(1)
    print("Found response tab")
    pag.hotkey('ctrl', 'a')
    time.sleep(1)
    pag.hotkey('ctrl', 'c')
    time.sleep(1)

    # write the clipboard to a text file and add the best encoding
    print("Writing to file")
    # with open(f'data/pageNum{pageNumber}.json', 'w', encoding='utf-8') as f:
    #     f.write(pyperclip.paste())

    print("Success! Moving to next page")

    
    time.sleep(1)
    
    # Call the function to scroll to the bottom
    locationViaImage('nextbutton.png', max_attempts=3, confidence=0.85)
    time.sleep(1)

    # presses