from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    """Set up Chrome WebDriver with proper configuration"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main():
    """Main function for message automation"""
    driver = None
    try:
        # Open LinkedIn in a new Chrome window
        driver = setup_driver()
        driver.get("https://www.linkedin.com/")

        # Log in to LinkedIn
        email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_key"))
        )
        password = driver.find_element(By.ID, "session_password")
        email.send_keys("your_email_address")
        password.send_keys("your_password")
        driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()

        # Wait for the page to load and navigate to the Messages page
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, "msg-overlay-list-bubble--conversation").click()

        # Search for the user you want to message and open their profile
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_box.send_keys("User's Name")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
