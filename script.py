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
        
        # Click the upload button
        upload_button.click()

         # Locate the file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fileOpen'))  # Adjust ID as per your HTML structure
        )
    
        # Provide the path of the file to upload
        file_path = '/home/toobler/projects/automationScriptIFC/0f887018aee343c19f9361baef346187.ifc'  # Replace with your actual file path
        file_input.send_keys(file_path)
        WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@id="uploadSuccessMessage"]'))
        )
        # screenshot_path = "/home/toobler/projects/automationScriptIFC/screenshot.png"  # Replace with your desired path
        # driver.save_screenshot(screenshot_path)

        
        # driver.find_element(By.LINK_TEXT, "Upload").click()
        # driver.find_element(By.ID, "wpUploadFile").send_keys(ifc_file_path)
        # driver.find_element(By.ID, "wpUploadFile").submit()
        
        # # Wait for the upload to complete (adjust time or use WebDriverWait for better handling)
        time.sleep(10)
        
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
