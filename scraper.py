from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_dummy_case_data(state, district, court, case_type, case_number, year):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Remove this line to see browser
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

        wait = WebDriverWait(driver, 15)

        # Click "Case Status"
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()

        # State
        Select(wait.until(EC.element_to_be_clickable((By.ID, "sess_state_code")))).select_by_visible_text(state)

        # Wait for District dropdown to populate
        time.sleep(2)
        Select(driver.find_element(By.ID, "sess_dist_code")).select_by_visible_text(district)

        # Wait for Court dr
