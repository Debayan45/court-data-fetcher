from flask import Flask, render_template, request
from scraper import fetch_case_data
from database import log_query

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        year = request.form['year']

        try:
            result = fetch_case_data(case_type, case_number, year)
            log_query(case_type, case_number, year, result['raw_html'])
            return render_template('index.html', data=result)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
