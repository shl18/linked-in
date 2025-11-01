import utils.net
import utils.clients
import utils.http_session
import utils.transport
import utils.session
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Check if we have a custom config path from environment variable
config_path = os.environ.get('CONFIG_PATH', 'config.py')

if config_path != 'config.py' and os.path.exists(config_path):
    # Import from temporary config file
    import sys
    import importlib.util
    spec = importlib.util.spec_from_file_location("temp_config", config_path)
    temp_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temp_config)
    
    username = temp_config.username
    password = temp_config.password
    MESSAGE_TEMPLATE = temp_config.MESSAGE_TEMPLATE
    TARGET_PROFILE_URL = temp_config.TARGET_PROFILE_URL
    TARGET_NAME = temp_config.TARGET_NAME
    TARGET_INDUSTRY = temp_config.TARGET_INDUSTRY
    HEADLESS_MODE = temp_config.HEADLESS_MODE
    BROWSER_WAIT_TIME = temp_config.BROWSER_WAIT_TIME
else:
    # Import from default config
    from config import (
        username, password, MESSAGE_TEMPLATE, TARGET_PROFILE_URL, 
        TARGET_NAME, TARGET_INDUSTRY, HEADLESS_MODE, BROWSER_WAIT_TIME
    )

def setup_driver():
    """Set up Chrome WebDriver with proper configuration"""
    try:
        options = webdriver.ChromeOptions()
        
        if HEADLESS_MODE:
            options.add_argument("--headless")
        
        # Add more stability options
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        print("Installing/updating ChromeDriver...")
        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("Chrome WebDriver setup successful!")
        return driver
        
    except Exception as e:
        print(f"Failed to setup Chrome WebDriver: {e}")
        print("Trying alternative setup...")
        
        # Fallback: try without webdriver-manager
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=options)
            print("Chrome WebDriver setup successful with fallback method!")
            return driver
            
        except Exception as e2:
            print(f"Fallback also failed: {e2}")
            raise Exception("Could not setup Chrome WebDriver. Please ensure Chrome is installed.")

def login_to_linkedin(driver):
    """Log in to LinkedIn with credentials from config"""
    try:
        print("Navigating to LinkedIn login page...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)  # Give page time to load
        
        print("Filling in login credentials...")
        # Wait for and fill username field
        username_field = WebDriverWait(driver, BROWSER_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "session_key"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        # Fill password field
        password_field = driver.find_element(By.NAME, "session_password")
        password_field.clear()
        password_field.send_keys(password)
        
        print("Submitting login form...")
        password_field.submit()
        
        # Wait for login to complete - check for either success or failure
        try:
            # Wait for either the main LinkedIn page or an error message
            WebDriverWait(driver, BROWSER_WAIT_TIME).until(
                lambda driver: "feed" in driver.current_url or "challenge" in driver.current_url or "login" not in driver.current_url
            )
            
            # Check if we're still on login page (login failed)
            if "login" in driver.current_url:
                print("Login failed - still on login page")
                return False
                
            print("Successfully logged in to LinkedIn")
            return True
            
        except Exception as wait_error:
            print(f"Login verification failed: {wait_error}")
            # Check current URL to see what happened
            print(f"Current URL: {driver.current_url}")
            return False
        
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def navigate_and_message_user(driver):
    """Navigate directly to user profile and send them a message"""
    try:
        print(f"Navigating directly to profile: {TARGET_PROFILE_URL}")
        driver.get(TARGET_PROFILE_URL)
        time.sleep(8)  # Wait longer for profile to load completely
        
        # Scroll down a bit to ensure all elements are loaded
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)
        
        # Try to find and click message button with multiple selectors
        message_selectors = [
            '//*[@id="ember305"]/span',  # Specific XPath you provided
            '//*[@id="ember300"]',  # Previous XPath
            '//span[text()="Message"]',
            '//button[contains(text(), "Message")]',
            '//a[contains(text(), "Message")]',
            '//button[@data-control-name="overlay.contact_card"]',
            '//div[contains(@class, "message-overlay")]//button',
            '//button[contains(@class, "message-overlay")]',
            '//div[@data-control-name="overlay.contact_card"]//button',
            '//button[contains(@aria-label, "Message")]'
        ]
        
        # Debug: Print current page source to see what's available
        print("Current page URL:", driver.current_url)
        
        # Look for any elements containing "Message" or "Connect"
        try:
            all_buttons = driver.find_elements(By.XPATH, "//button | //a | //span")
            print("Available buttons/links on page:")
            for i, btn in enumerate(all_buttons[:10]):  # Show first 10
                try:
                    text = btn.text.strip()
                    if text and ("Message" in text or "Connect" in text or "Follow" in text):
                        print(f"  {i}: {text} - {btn.tag_name}")
                except:
                    pass
        except Exception as e:
            print(f"Debug info error: {e}")
        
        message_button = None
        for selector in message_selectors:
            try:
                message_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found message button with selector: {selector}")
                break
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                continue
        
        if not message_button:
            print("Could not find message button. The user might not allow direct messages.")
            print("Trying alternative approach...")
            
            # Try to find Connect button first
            connect_selectors = [
                '//span[text()="Connect"]',
                '//button[contains(text(), "Connect")]',
                '//button[@data-control-name="connect"]'
            ]
            
            connect_button = None
            for selector in connect_selectors:
                try:
                    connect_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found Connect button with selector: {selector}")
                    break
                except:
                    continue
            
            if connect_button:
                print("Clicking Connect button...")
                connect_button.click()
                time.sleep(3)
                
                # After connecting, try to find message button again
                for selector in message_selectors:
                    try:
                        message_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"Found message button after connect: {selector}")
                        break
                    except:
                        continue
        
        if not message_button:
            print("Could not find message button even after trying Connect")
            return False
            
        print("Clicking message button...")
        message_button.click()
        time.sleep(3)
        
        # Try to find message input field
        message_input_selectors = [
            '//div[@contenteditable="true"]',
            '//div[contains(@class, "msg-form__contenteditable")]',
            '//div[@role="textbox"]',
            '//textarea[@aria-label="Write a message…"]',
            '//textarea[@placeholder="Write a message…"]',
            '//textarea[contains(@class, "msg-form__contenteditable")]',
            '//div[contains(@class, "msg-form__contenteditable")]',
            '//div[@data-placeholder="Write a message…"]',
            '//div[contains(@class, "msg-form__contenteditable")]//div[@contenteditable="true"]'
        ]
        
        # Debug: Look for any input elements
        try:
            all_inputs = driver.find_elements(By.XPATH, "//input | //textarea | //div[@contenteditable='true']")
            print("Available input elements:")
            for i, inp in enumerate(all_inputs[:5]):  # Show first 5
                try:
                    tag = inp.tag_name
                    placeholder = inp.get_attribute("placeholder") or inp.get_attribute("data-placeholder") or "No placeholder"
                    print(f"  {i}: {tag} - {placeholder}")
                except:
                    pass
        except Exception as e:
            print(f"Debug input info error: {e}")
        
        message_box = None
        for selector in message_input_selectors:
            try:
                message_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"Found message box with selector: {selector}")
                break
            except Exception as e:
                print(f"Input selector {selector} failed: {e}")
                continue
        
        if not message_box:
            print("Could not find message input field")
            return False
        
        # Format and send message
        message = MESSAGE_TEMPLATE.format(name=TARGET_NAME, industry=TARGET_INDUSTRY)
        print(f"Sending message: {message}")
        
        message_box.clear()
        message_box.send_keys(message)
        time.sleep(2)
        message_box.send_keys(Keys.RETURN)
        
        print(f"Message sent successfully to {TARGET_NAME}")
        return True
        
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False

def main():
    """Main function to run the LinkedIn bot"""
    driver = None
    try:
        print("Setting up Chrome WebDriver...")
        driver = setup_driver()
        
        print("Logging in to LinkedIn...")
        if not login_to_linkedin(driver):
            return
        
        print(f"Navigating to profile and sending message...")
        if not navigate_and_message_user(driver):
            return
            
        print("Bot execution completed successfully!")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()

if __name__ == "__main__":
    main()