from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def fetch_case_data(case_type, case_number, year):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    service = Service(executable_path="chromedriver")  # or give full path here
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&state=D&dist=9")

    wait = WebDriverWait(driver, 10)

    try:
        # Wait for dropdowns and inputs
        wait.until(EC.presence_of_element_located((By.NAME, "case_type")))

        # Fill form
        Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)
        driver.find_element(By.NAME, "case_no").send_keys(case_number)
        driver.find_element(By.NAME, "case_year").send_keys(year)

        # Wait for CAPTCHA if present
        time.sleep(2)
        try:
            captcha_input = driver.find_element(By.NAME, "captcha_val")
            captcha_text = input("🛑 CAPTCHA is present. Check the browser window and enter the value here: ")
            captcha_input.send_keys(captcha_text)
        except:
            pass  # No CAPTCHA

        # Submit
        driver.find_element(By.NAME, "submit").click()

        # Wait for results
        wait.until(EC.presence_of_element_located((By.ID, "petresp")))

        # Parse results
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        raw_html = soup.prettify()

        parties = soup.find("span", {"id": "petresp"}).text.strip() if soup.find("span", {"id": "petresp"}) else "N/A"
        filing_date = soup.find("span", {"id": "fdate"}).text.strip() if soup.find("span", {"id": "fdate"}) else "N/A"
        next_hearing = soup.find("span", {"id": "nhearing"}).text.strip() if soup.find("span", {"id": "nhearing"}) else "N/A"
        order_link_tag = soup.find("a", href=True, string="View")
        latest_order_link = "https://services.ecourts.gov.in" + order_link_tag['href'] if order_link_tag else "#"

        driver.quit()

        return {
            'case_title': f'{case_type}/{case_number}/{year}',
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': latest_order_link,
            'raw_html': raw_html
        }

    except Exception as e:
        driver.quit()
        raise Exception(f"[Selenium error] {str(e)}")
