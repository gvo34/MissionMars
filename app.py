from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

#mongo = PyMongo(app)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.marsDB
collection = db.marsnews



@app.route("/")
def index():
    #marsnews = mongo.db.marsDB.find_one()
    mars_data = collection.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():
    scrape_mars.scrape()
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
