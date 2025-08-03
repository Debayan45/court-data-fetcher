def fetch_dummy_case_data(state, district, court, case_type, case_number, year):
    return {
        'case_title': f'{case_type}/{case_number}/{year}',
        'state': state,
        'district': district,
        'court': court,
        'parties': 'ABC vs XYZ',
        'filing_date': '2023-01-10',
        'next_hearing': '2025-09-12',
        'latest_order_link': 'https://example.com/order.pdf',
    }
