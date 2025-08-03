from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

def fetch_case_data(case_type, case_number, year):
    # Set up headless Chrome (you can remove headless to see the browser)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&state=D&dist=9"
    driver.get(url)

    try:
        time.sleep(2)

        # Fill the form
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
        driver.find_element(By.ID, "case_no").clear()
        driver.find_element(By.ID, "case_no").send_keys(case_number)
        driver.find_element(By.ID, "case_year").clear()
        driver.find_element(By.ID, "case_year").send_keys(year)

        # Submit the form
        driver.find_element(By.NAME, "submit").click()
        time.sleep(3)  # Let the page load

        # Check if case exists
        if "No Record Found" in driver.page_source:
            driver.quit()
            raise Exception("No record found for given case details.")

        # Extract relevant fields
        parties = driver.find_element(By.ID, "petresp").text.strip() if driver.find_elements(By.ID, "petresp") else "N/A"
        filing_date = driver.find_element(By.ID, "fdate").text.strip() if driver.find_elements(By.ID, "fdate") else "N/A"
        next_hearing = driver.find_element(By.ID, "nhearing").text.strip() if driver.find_elements(By.ID, "nhearing") else "N/A"
        order_link = driver.find_elements(By.LINK_TEXT, "View")
        latest_order_link = order_link[0].get_attribute("href") if order_link else "#"

        result = {
            'case_title': f"{case_type}/{case_number}/{year}",
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': latest_order_link,
            'raw_html': driver.page_source[:500]  # Store partial HTML for debug
        }

        driver.quit()
        return result

    except Exception as e:
        driver.quit()
        raise Exception(f"❌ Error: {str(e)}")
