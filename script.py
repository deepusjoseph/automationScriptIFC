from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException  # Import TimeoutException
from selenium.webdriver import ActionChains
import time
import openai
import pyautogui
import os

# Initialize the OpenAI API client
openai.api_key = 'your_openai_api_key'

def upload_and_screenshot(ifc_file_path):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Open Wiki IFC
        driver.get('https://wikiifc.com/')
        
        # Interact with the page to upload the IFC file (adjust selectors as needed)
       # Wait for the button to be clickable
        guest_login_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="enterAsGuest" and contains(@class, "landing-secondary")]'))
        )
        guest_login_button.click()
        # WebDriverWait(driver, 10).until(
        # EC.visibility_of_element_located((By.XPATH, '//div[@id="guestLoginSuccessMessage"]'))
        # )
        # Wait for the upload button to be clickable
        upload_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'btnUpload'))
        )
        # Scroll the upload button into view if needed
        # driver.execute_script("arguments[0].scrollIntoView();", upload_button)
        
        # time.sleep(5)
        # Click the upload button
        upload_button.click()

        time.sleep(3)
        file_path = '/home/toobler/Downloads/train/0f887018aee343c19f9361baef346187.ifc'  # Replace with your actual file path
        pyautogui.write(file_path)
        time.sleep(3)
        pyautogui.press('enter')

        # Use JavaScript to get the bounding rectangle of the canvas element
        bounding_rect = driver.execute_script("""
        const canvas = document.querySelector('canvas');  // Adjust the selector as per your HTML structure
        const rect = canvas.getBoundingClientRect();
        const windowX = window.screenX;
        const windowY = window.screenY;
         const outerHeight = window.outerHeight - window.innerHeight;
    const outerWidth = window.outerWidth - window.innerWidth;
    return {
        x: rect.left + windowX + outerWidth / 2,
        y: rect.top + windowY + outerHeight,
        width: rect.width,
        height: rect.height
    };
    """)

        # Get the bounding rectangle properties
        x = int(bounding_rect['x'])
        y = int(bounding_rect['y'])
        width = int(bounding_rect['width'])
        height = int(bounding_rect['height'])

        # Wait a bit to ensure the canvas is fully rendered
        time.sleep(2)

        # Take a screenshot using pyautogui
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        time.sleep(2)

        # Save the screenshot
        save_path = os.path.expanduser('/home/toobler/Documents/codebase/automate/automationScriptIFC/1.png')
        print(save_path)
        time.sleep(2)
        screenshot.save(save_path)  

         # Locate the file input element
        # file_input = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, 'fileOpen'))  # Adjust ID as per your HTML structure
        # )

        # print('fileinput')
        # print(file_input)
    
        # # Provide the path of the file to upload
        # file_input.send_keys(file_path)
        # WebDriverWait(driver, 20).until(
        # EC.visibility_of_element_located((By.XPATH, '//div[@id="uploadSuccessMessage"]'))
        # )
        # screenshot_path = "/home/toobler/projects/automationScriptIFC/screenshot.png"  # Replace with your desired path
        # driver.save_screenshot(screenshot_path)

        
        # driver.find_element(By.LINK_TEXT, "Upload").click()
        # driver.find_element(By.ID, "wpUploadFile").send_keys(ifc_file_path)
        # driver.find_element(By.ID, "wpUploadFile").submit()
        
        # # Wait for the upload to complete (adjust time or use WebDriverWait for better handling)
        time.sleep(2)
        
        # # Take a screenshot
        # screenshot_path = "screenshot.png"
        # driver.save_screenshot(screenshot_path)
        
        # return screenshot_path
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    finally:
        driver.quit()

def get_description_from_chatgpt(image_path):
    # Open the screenshot file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    # Send the image to ChatGPT
    response = openai.Image.create(
        file=image_data,
        purpose="describe"
    )
    
    return response['choices'][0]['text']

if __name__ == "__main__":
    ifc_file_path = "path/to/your/ifc/file.ifc"
    screenshot_path = upload_and_screenshot(ifc_file_path)
    
    # description = get_description_from_chatgpt(screenshot_path)
    # print("Description from ChatGPT:", description)
