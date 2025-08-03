from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_court_data(state, district, court_complex, case_type, case_number, year):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index")
        wait = WebDriverWait(driver, 20)

        # Select State
        state_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sess_state_code")))
        Select(state_dropdown).select_by_visible_text(state)

        # Select District
        wait.until(EC.presence_of_element_located((By.ID, "sess_dist_code")))
        Select(driver.find_element(By.ID, "sess_dist_code")).select_by_visible_text(district)

        # Select Court Complex
        wait.until(EC.presence_of_element_located((By.ID, "court_complex_code")))
        Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text(court_complex)

        # Click on Case Number tab
        driver.find_element(By.XPATH, "//button[contains(text(), 'Case Number')]").click()

        # Fill Case Type, Case Number, Year
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
        driver.find_element(By.ID, "case_no").send_keys(case_number)
        Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(str(year))

        # Submit
        driver.find_element(By.ID, "searchbtn").click()

        # Wait and parse result
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "case_status_main")))
        result = driver.find_element(By.CLASS_NAME, "case_status_main").text

        return {"success": True, "result": result}

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.quit()
