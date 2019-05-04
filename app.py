from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")


@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars = mars)


@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
