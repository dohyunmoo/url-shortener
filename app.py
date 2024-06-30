from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import string
import random
import os

app = Flask(__name__, template_folder="static")
app.config["JSON_AS_DICT"] = True

client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
urls_collection = db["urls"]  # Specify the collection name

urls_collection.delete_many({"long_url": "aaaa"})

# Function to generate a unique short code
def generate_short_code():
    chars = string.ascii_lowercase + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(6))
        if not urls_collection.find_one({"short_code": code}):
            return code

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def shorten_url():
    long_url_data = request.get_json()
    long_url = long_url_data.get("long_url")
    print(long_url)

    if not long_url:
        return "Invalid URL format!", 400
    
    url = urls_collection.find_one({"long_url": long_url})
    if url:
        print(f"{long_url} exists already")
        return jsonify({"short_url": f"/{url['short_code']}"})

    short_code = generate_short_code()
    new_url = {"long_url": long_url, "short_code": short_code}
    urls_collection.insert_one(new_url)
    short_url = url_for('redirect_url', short_code=short_code)

    # return render_template('success.html', short_url=short_url)
    return jsonify({"short_url": short_url}) # data sent to index.html

@app.route('/<short_code>')
def redirect_url(short_code):
    for document in urls_collection.find({}):
        print(document)

    url = urls_collection.find_one({"short_code": short_code})
    if url:
        return redirect(url["long_url"])
    else:
        # create and render a custom 404 not found page
        # return "404 Not Found", 404
        return render_template("failure.html", short_url=short_code)

if __name__ == '__main__':
    app.run(debug=True)
