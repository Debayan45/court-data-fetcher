from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def fetch_case_data(case_type, case_number, year):
    # Set up headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&state=D&dist=9")

        wait = WebDriverWait(driver, 10)

        # Select case type
        Select(wait.until(EC.presence_of_element_located((By.NAME, "case_type")))).select_by_visible_text(case_type)

        # Fill in case number and year
        driver.find_element(By.NAME, "case_no").send_keys(case_number)
        driver.find_element(By.NAME, "case_year").send_keys(year)

        # Submit form
        driver.find_element(By.NAME, "submit").click()

        # Wait for result to load
        wait.until(EC.presence_of_element_located((By.ID, "petresp")))

        parties = driver.find_element(By.ID, "petresp").text.strip()
        filing_date = driver.find_element(By.ID, "fdate").text.strip()
        next_hearing = driver.find_element(By.ID, "nhearing").text.strip()

        # Find link to latest order
        try:
            link = driver.find_element(By.LINK_TEXT, "View")
            latest_order_link = "https://services.ecourts.gov.in" + link.get_attribute('href')
        except:
            latest_order_link = "#"

        raw_html = driver.page_source

        return {
            'case_title': f'{case_type}/{case_number}/{year}',
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': latest_order_link,
            'raw_html': raw_html
        }

    except TimeoutException:
        raise Exception("Timeout while loading court data.")
    finally:
        driver.quit()
