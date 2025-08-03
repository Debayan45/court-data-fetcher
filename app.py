from flask import Flask, render_template, request
from scraper import fetch_dummy_case_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        state = request.form['state']
        district = request.form['district']
        court = request.form['court']
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        year = request.form['year']

        result = fetch_dummy_case_data(state, district, court, case_type, case_number, year)
        return render_template('index.html', data=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
