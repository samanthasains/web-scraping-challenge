# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:42:00 2020

@author: saman
"""

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

   # Run the scrape function and save the results to a variable
   mars_dict=mongo.db.mars_dict
   mars_data=scrape_mars.scrape()

   # Update the Mongo database using update and upsert=True
   mars_dict.update({}, mars_data, upsert=True)

   # Redirect back to home page
   return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)