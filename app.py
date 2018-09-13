from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# use a flask app
app = Flask(__name__)

# use a local mongodb
mongo = PyMongo(app) 

@app.route("/")
def index():
    # collect data from DB to complete index.html
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars_data=mars)


@app.route("/scrape")
def scrape():
    # webscraping to collect new data
    marsdata = scrape_mars.scrape()

    # store newly scrapped content into DB
    mars = mongo.db.mars
    mars.update(
        {},
        marsdata,
        upsert=True
    )
    
    # refresh index.html page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
