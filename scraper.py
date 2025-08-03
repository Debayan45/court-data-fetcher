from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

def fetch_case_data(case_type, case_number, year):
    options = Options()
    options.add_experimental_option("detach", True)  # Keep browser open

    driver = webdriver.Chrome(options=options)
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&state=D&dist=9")

    try:
        # Wait for page to load
        time.sleep(3)

        # Select case type
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

        # Fill in case number and year
        driver.find_element(By.ID, "case_no").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(year)

        print("👉 Please solve the CAPTCHA manually in the opened browser.")
        input("✅ Press ENTER here *after* submitting the form manually...")

        time.sleep(5)  # Allow time for page to load

        # Now extract data
        parties = driver.find_element(By.ID, "petresp").text.strip() if driver.find_elements(By.ID, "petresp") else "N/A"
        filing_date = driver.find_element(By.ID, "fdate").text.strip() if driver.find_elements(By.ID, "fdate") else "N/A"
        next_hearing = driver.find_element(By.ID, "nhearing").text.strip() if driver.find_elements(By.ID, "nhearing") else "N/A"

        # Order link
        link_element = driver.find_elements(By.LINK_TEXT, "View")
        latest_order_link = link_element[0].get_attribute("href") if link_element else "#"

        driver.quit()

        return {
            'case_title': f'{case_type}/{case_number}/{year}',
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': latest_order_link,
            'raw_html': "(Selenium handled, not raw HTML)"
        }

    except Exception as e:
        driver.quit()
        raise Exception(f"Selenium scraping failed: {str(e)}")
