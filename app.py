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

# Function to generate a unique short code
def generate_short_code():
    supported = {
        "A": [i for i in range(128512, 128592)] + [i for i in range(128640, 128704)],
        "B": [9994, 9995, 9996],
        "C":  [i for i in range(127745, 128281)] + [128293]
    }

    while True:
        char1_int = supported["A"][random.randint(0, len(supported["A"]) - 1)]
        char2_int = supported["A"][random.randint(0, len(supported["A"]) - 1)]
        char3_int = supported["B"][random.randint(0, len(supported["B"]) - 1)]
        char4_int = supported["C"][random.randint(0, len(supported["C"]) - 1)]

        char1_hex = hex(char1_int)
        char2_hex = hex(char2_int)
        char3_hex = hex(char3_int)
        char4_hex = hex(char4_int)

        short_code = f"{char1_hex[2:]}{char2_hex[2:]}{char3_hex[2:]}{char4_hex[2:]}"
        
        if not urls_collection.find_one({"short_code": short_code}):
            char1 = chr(char1_int)
            char2 = chr(char2_int)
            char3 = chr(char3_int)
            char4 = chr(char4_int)
            return short_code, f"{char1}{char2}{char3}{char4}"


    # chars = string.ascii_lowercase + string.digits
    # while True:
    #     code = ''.join(random.choice(chars) for _ in range(6))
    #     if not urls_collection.find_one({"short_code": code}):
    #         return code

def decode(hex_string):
    if len(hex_string) != 19:
        return None
    c1 = chr(int(f'0x{hex_string[0:5]}', 0))
    c2 = chr(int(f'0x{hex_string[5:10]}', 0))
    c3 = chr(int(f'0x{hex_string[10:14]}', 0))
    c4 = chr(int(f'0x{hex_string[14:]}', 0))
    return f"{c1}{c2}{c3}{c4}"

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
        emoji_code = decode(url["short_code"])
        return jsonify({"short_url": f"/{url['short_code']}", "emoji_code": emoji_code})

    short_code, emoji_code = generate_short_code()
    new_url = {"long_url": long_url, "short_code": short_code}
    urls_collection.insert_one(new_url)
    short_url = url_for("redirect_url", short_code=short_code)

    # return render_template('success.html', short_url=short_url)
    return jsonify({
        "short_url": short_url,
        "emoji_code": emoji_code
    }) # data sent to index.html

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
        return render_template("failure.html", short_url=short_code, emoji_url=decode(short_code))

if __name__ == "__main__":
    app.run()
    # generate_short_code()
