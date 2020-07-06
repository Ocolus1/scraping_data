from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


app = Flask(__name__)
app.config.update(
    #Set the secret key to a sufficiently random value
    SECRET_KEY=os.urandom(24)
)


@app.route("/", methods=['POST','GET'])
@app.route("/home", methods=['POST','GET'])
@app.route("/index", methods=['POST','GET'])
def home():
    if request.method == "POST":
        keyword = request.form['keyword']
        location = request.form['location']
        try:
            url = 'https://www.monster.com/jobs/search/?q={keyword}&where={location}&intcid=skr_navigation_nhpso_searchMain'.format(
                keyword = keyword,
                location= location
            )
            page = requests.get(url)
            

            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id="ResultsContainer")

            job_elems = results.find_all('section', class_="card-content")
            return render_template('home.htm', job_elems=job_elems)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return render_template('home.htm', e=e)

    return render_template('home.htm')


if __name__ == "__main__":
    app.run(debug=True)