from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def fetch_case_data(case_type, case_number, year):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Comment this line for visual debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&state=D&dist=9")

        wait = WebDriverWait(driver, 10)

        # Select case type
        case_type_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "case_type")))
        Select(case_type_dropdown).select_by_visible_text(case_type)

        # Enter case number
        driver.find_element(By.NAME, "case_no").clear()
        driver.find_element(By.NAME, "case_no").send_keys(case_number)

        # Enter case year
        driver.find_element(By.NAME, "case_year").clear()
        driver.find_element(By.NAME, "case_year").send_keys(year)

        # Submit the form
        driver.find_elem_
