import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

def main():
    # Retrieve command-line arguments
    if len(sys.argv) != 7:
        print("Usage: python linkedin.py <username> <password> <search_term> <company_name> <num_pages> <personalized_message>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    search_term = sys.argv[3]
    company_name = sys.argv[4]
    num_pages = int(sys.argv[5])
    personalized_message = sys.argv[6]

    # Set up the Chrome webdriver
    chrome_driver_path = 'chromedriver.exe'  # Update this path as needed
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Open LinkedIn website
        url = "https://www.linkedin.com/"
        driver.get(url)
        time.sleep(2)  # Add a delay for the page to load

        sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
        sign_in_button.click()
        time.sleep(2)  # Add a delay for the next page to load

        # Locate and fill in the login details (modify based on LinkedIn login fields)
        email_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")

        # Input email and password
        email_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(25)  # Add a delay for the next page to load after login

        search_input = driver.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input")
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Click on 'People' button and wait
        people_buttons = driver.find_elements(By.CSS_SELECTOR, "button.search-reusables__filter-pill-button")

        for button in people_buttons:
            if button.text.strip() == "People":
                button.click()
                time.sleep(2) 
                break

        # Click on 'All filters' button
        all_filters_button = driver.find_element(By.CSS_SELECTOR, "button.search-reusables__all-filters-pill-button")
        all_filters_button.click()
        time.sleep(5)

        invite_dialog = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a11y-text")))
        driver.execute_script("arguments[0].scrollIntoView(true);", invite_dialog)

        # Find the div containing the company checkboxes
        company_values = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-reusables__secondary-filters-values")))
        time.sleep(2)

        # Click 'Add a company' button within the dialog
        add_company_button = company_values.find_element(By.XPATH, "//span[text()='Add a company']")
        add_company_button.click()
        time.sleep(2)

        # Enter personalized text in the input field
        input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Add a company']")))
        input_field.send_keys(company_name)
        time.sleep(2)

        driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        time.sleep(2)

        input_field = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Add a company']")))
        input_field.click()

        # Simulate pressing the down arrow key to navigate to the first item
        input_field.send_keys(Keys.ARROW_DOWN)

        # Simulate pressing Enter to select the highlighted item
        input_field.send_keys(Keys.ENTER)

        # Click 'Show results' button to close the popup
        show_results_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show results']")))
        show_results_button.click()
        time.sleep(2)

        num_pages = num_pages

        for _ in range(num_pages):
            # Find and click 'Connect' buttons for all profiles on the page
            while True:
                connect_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view:not([class*='--muted']):not([class*='--circle'])")))
                profile_name_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[dir='ltr']")))
                profile_name_elements = [prof.text.split()[0] for prof in profile_name_elements if any(c.isalpha() for c in prof.text)]
                profile_connect_dict = {}

                for profile_name, connect_button in zip(profile_name_elements, connect_buttons):
                    if connect_button.text.strip() == "Connect":
                        profile_connect_dict[profile_name] = connect_button

                if not profile_connect_dict: 
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next']")))
                    #Scroll into view and click the 'Next' button
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    next_button.click()  # Break the loop after clicking the 'Next' button
                    time.sleep(15) # Break the loop if no profiles with 'Connect' button found
                    break

                for profile_name, connect_button in profile_connect_dict.items():
                    try:
                        connect_button.click()
                        time.sleep(2)

                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "send-invite-modal")))

                        invite_dialog = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.artdeco-modal--layer-default.send-invite")))

                        add_note_button = invite_dialog.find_element(By.CSS_SELECTOR, "button[aria-label='Add a note']")
                        if add_note_button.text.strip() == "Add a note":
                            add_note_button.click()

                            note_text_area = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='message']")))
                            note_text_1 = f"Hello {profile_name},"
                            note_text_2 = personalized_message
                            note_text_area.send_keys(note_text_1)
                            note_text_area.send_keys(Keys.ENTER)
                            note_text_area.send_keys(note_text_2)
                            time.sleep(4)

                            send_button = None
                            for _ in range(10):  # Max 10 attempts with a delay of 2 seconds between attempts
                                try:
                                    send_button = invite_dialog.find_element(By.CSS_SELECTOR, "button[aria-label='Send now']")
                                    break  # If found, exit the loop
                                except NoSuchElementException:
                                    time.sleep(2)  # Wait for 2 seconds before rechecking
                                    continue

                            if send_button:
                                send_button.click()
                                time.sleep(3)  # Add a small delay after clicking Send button

                                # Scroll to load more profiles
                                driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
                                time.sleep(2)  # Add a delay after scrolling to load more profiles

                    except ElementClickInterceptedException:
                        print("Element click intercepted, retrying after delay")
                        time.sleep(5)  # Add a delay before retrying to click the button
                        continue

                next_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button span.artdeco-button__text")))

                for button in next_buttons:
                    if button.text.strip() == "Next":
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)  # Add a small delay after scrolling

                        button.click()
                        print("Next button clicked")
                        break  # Break the loop after clicking the 'Next' button
                time.sleep(5)
                break        
    finally:
        # Close the browser window
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()









