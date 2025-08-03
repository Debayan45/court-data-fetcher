import requests
from bs4 import BeautifulSoup

def fetch_case_data(case_type, case_number, year):
    # Step 1: Form URL and headers
    url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index&state=D&dist=9"

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    payload = {
        "stateCode": "D",  # D for Delhi (or try with HR for Haryana)
        "distCode": "9",   # 9 = Faridabad
        "courtCode": "0",  # Generic
        "case_type": case_type,
        "case_no": case_number,
        "case_year": year,
        "submit": "Submit"
    }

    try:
        session = requests.Session()
        response = session.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        raw_html = soup.prettify()

        # Parse mock data to test response
        parties = soup.find("span", {"id": "petresp"}).text.strip() if soup.find("span", {"id": "petresp"}) else "N/A"
        filing_date = soup.find("span", {"id": "fdate"}).text.strip() if soup.find("span", {"id": "fdate"}) else "N/A"
        next_hearing = soup.find("span", {"id": "nhearing"}).text.strip() if soup.find("span", {"id": "nhearing"}) else "N/A"

        # Find PDF order links
        link = soup.find("a", href=True, string="View")
        latest_order_link = "https://services.ecourts.gov.in" + link['href'] if link else "#"

        return {
            'case_title': f'{case_type}/{case_number}/{year}',
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': latest_order_link,
            'raw_html': raw_html
        }

    except Exception as e:
        raise Exception(f"Scraper failed: {str(e)}")
