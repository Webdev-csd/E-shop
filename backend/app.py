import os
from random import randint

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint
from bson import ObjectId

app = Flask(__name__)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "MongoDB API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

CORS(app)

MONGODB_HOST = os.getenv("MONGODB_HOST", "mongo")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_USER = os.getenv("MONGODB_USER", "root")
MONGODB_PASS = os.getenv("MONGODB_PASS", "example")

client = MongoClient(
    MONGODB_HOST, MONGODB_PORT, username=MONGODB_USER, password=MONGODB_PASS
)

db = client.eshop_db
products = db.products

products.create_index([("name", "text")])

default_products = [
    {
        "name": "Dolce & Banana Krasaraaaa",
        "image_url": "/static/images/tshirt_1.jpg",
        "description": "A comfortable cotton t-shirt for the light drinkers.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Dolce & Banana T-shirt",
        "image_url": "/static/images/tshirt_2.jpg",
        "description": "A stylish t-shirt with a unique design.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Dolce & Banana Van Life",
        "image_url": "/static/images/tshirt_3.jpg",
        "description": "A white t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Dolce & Banana Kali",
        "image_url": "/static/images/tshirt_4.jpg",
        "description": "A trendy t-shirt for the open minded.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Guccy T-shirt",
        "image_url": "/static/images/tshirt_5.jpg",
        "description": "A playful t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Guccy NYC",
        "image_url": "/static/images/tshirt_6.jpg",
        "description": "A dreamy blue t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Guccy Black Canvas",
        "image_url": "/static/images/tshirt_7.jpg",
        "description": "A --- t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Guccy Bowling Shirt",
        "image_url": "/static/images/tshirt_8.jpg",
        "description": "For late Friday nights.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Channel L.A.",
        "image_url": "/static/images/tshirt_9.jpg",
        "description": "A trendy black t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Channel Pac-Man",
        "image_url": "/static/images/tshirt_10.jpg",
        "description": "A retro yellow t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "Channel Space Invaders",
        "image_url": "/static/images/tshirt_11.jpg",
        "description": "A fantastic t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Channel T-shirt",
        "image_url": "/static/images/tshirt_12.jpg",
        "description": "Another trendy black t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Versabe Sporty Purple",
        "image_url": "/static/images/tshirt_13.jpg",
        "description": "For the gym rats.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Versabe B&B T-shirt",
        "image_url": "/static/images/tshirt_14.jpg",
        "description": "A stylish Beige & Black t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Versabe Nirvana Limited Edition",
        "image_url": "/static/images/tshirt_15.jpg",
        "description": "For the old-timers.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Versabe Crossover",
        "image_url": "/static/images/tshirt_16.jpg",
        "description": "Somethin special.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Adibas Colorful Blue & White",
        "image_url": "/static/images/tshirt_17.jpg",
        "description": "A comfortable t-shirt in two colours.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Adibas T-shirt",
        "image_url": "/static/images/tshirt_18.jpg",
        "description": "Nothing more, nothing less. Just a t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Adibas Aquas",
        "image_url": "/static/images/tshirt_19.jpg",
        "description": "Always remember to stay hydrated.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "Adibas Bossita",
        "image_url": "/static/images/tshirt_20.jpg",
        "description": "Yasss.",
        "likes": randint(0, 100),
        "price": 24.99,
    }
]

if products.count_documents({}) == 0:
    products.insert_many(default_products)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")  # Get search query from request
    search_results = []
    # Handle empty search query
    if not query:
        search_results = products.find()
    else:
        search_results = products.find(
            {"name": {"$regex": query, "$options": "i"}}  # Case-insensitive search
        )
    # Sort by price in descending order
    search_results.sort("price", -1)  

    # Convert MongoDB documents to JSON-serializable format
    results_list = []
    for product in search_results:
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        results_list.append(product)

    return jsonify(list(results_list))



@app.route("/like", methods=["POST"])
def like():
    data = request.get_json()
    product_id = data.get("_id")

    products.update_one( 
        {"_id": ObjectId(product_id)},
        {"$inc": {"likes":1} } )
    
    updated_product = products.find_one({"_id": ObjectId(product_id)})
    updated_likes = updated_product.get("likes",0)

    return jsonify({"success": True , "updated_likes": updated_likes})



@app.route("/popular_products", methods=["GET"])
def popular_products():

    top_5 = products.find().sort("likes", -1).limit(5)
    results = []
    for product in top_5:
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        results.append(product)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
