from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

# Function to take a screenshot on failure
def take_screenshot(driver, Screenshoot):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    file_path = os.path.join("screenshots", Screenshoot)
    driver.save_screenshot(file_path)
    print(f"Screenshot saved to {file_path}")

# Positive Scenario: Valid Login
def test_positive_login(driver):
    driver.get("https://lapor.folkatech.com/")

    # Maximize the window
    driver.maximize_window()

    try:
        # Enter valid credentials
        username_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        username_field.send_keys("admin@example.com")
        password_field.send_keys("password")
        login_button.click()

        # Assert successful login
        time.sleep(2)  # Wait for the page to load
        dashboard_element = driver.find_element(By.ID, "sidenav-main")
        if dashboard_element.is_displayed():
            print("Positive Scenario: Login successful.")
    except NoSuchElementException as e:
        take_screenshot(driver, "positive_login_failure.png")
        print(f"Positive Scenario failed: {e}")
    finally:
        # Logout
        adminicon = driver.find_element(By.XPATH, '//*[@id="dropdownMenuButton"]/div/div[2]/img')
        Logout = driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li/ul/li[2]/a/div')
        adminicon.click()
        Logout.click()
        time.sleep(2)
    


# Negative Scenario: Invalid Login
def test_negative_login(driver):
    driver.get("https://lapor.folkatech.com/")
    wait = WebDriverWait(driver, 10)

    # Maximize the window
    driver.maximize_window()

    try:
        # Enter invalid credentials
        username_field1 = driver.find_element(By.NAME, "email")
        password_field1 = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        username_field1.send_keys("invalid_username@email.com")
        password_field1.send_keys("invalid_password")
        login_button.click()

        # Assert error message is displayed
        time.sleep(2)
        alert_message = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@role='alert' and contains(@class, 'text-danger')]")))
        assert "Login Gagal! Akun tidak ada." in alert_message.text, "Pesan error tidak sesuai!"
        if alert_message.is_displayed():
            print("Negative Scenario: Error message displayed as expected.")
    except NoSuchElementException as e:
        take_screenshot(driver, "negative_login_failure.png")
        print(f"Negative Scenario failed: {e}")

# Main function
def main():
    driver = webdriver.Chrome()

    try:
        # Test scenarios
        test_positive_login(driver)
        test_negative_login(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()