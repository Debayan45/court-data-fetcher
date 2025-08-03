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

        # Wait for Court dropdown
        time.sleep(2)
        Select(driver.find_element(By.ID, "court_code")).select_by_visible_text(court)

        # Case Type
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

        # Case No and Year
        driver.find_element(By.ID, "case_no").send_keys(case_number)
        Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(year)

        # Manually solve CAPTCHA for now
        input("🛑 Please solve CAPTCHA in browser and press Enter to continue...")

        # Submit
        driver.find_element(By.NAME, "submit").click()
        time.sleep(5)

        # Extract basic details
        parties = driver.find_element(By.ID, "petresp").text
        filing_date = driver.find_element(By.ID, "fdate").text
        next_hearing = driver.find_element(By.ID, "nhearing").text
        try:
            link = driver.find_element(By.LINK_TEXT, "View").get_attribute("href")
        except:
            link = "#"

        return {
            'case_title': f'{case_type}/{case_number}/{year}',
            'state': state,
            'district': district,
            'court': court,
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': link,
        }

    except Exception as e:
        return {'error': str(e)}
    finally:
        driver.quit()
