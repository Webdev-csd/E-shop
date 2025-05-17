import os
from random import randint

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint

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
        "name": "T-shirt 1",
        "image_url": "/static/images/tshirt_1.jpg",
        "description": "A comfortable cotton t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 2",
        "image_url": "/static/images/tshirt_2.jpg",
        "description": "A stylish t-shirt with a unique design.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 3",
        "image_url": "/static/images/tshirt_3.jpg",
        "description": "A classic white t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 4",
        "image_url": "/static/images/tshirt_4.jpg",
        "description": "A trendy black t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 5",
        "image_url": "/static/images/tshirt_5.jpg",
        "description": "A vibrant red t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 6",
        "image_url": "/static/images/tshirt_6.jpg",
        "description": "A cool blue t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 7",
        "image_url": "/static/images/tshirt_7.jpg",
        "description": "A stylish green t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 8",
        "image_url": "/static/images/tshirt_8.jpg",
        "description": "A comfortable yellow t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 9",
        "image_url": "/static/images/tshirt_9.jpg",
        "description": "A trendy purple t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 10",
        "image_url": "/static/images/tshirt_10.jpg",
        "description": "A stylish orange t-shirt.",
        "likes": randint(0, 100),
        "price": 19.99,
    },
    {
        "name": "T-shirt 11",
        "image_url": "/static/images/tshirt_11.jpg",
        "description": "A comfortable pink t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 12",
        "image_url": "/static/images/tshirt_12.jpg",
        "description": "A trendy gray t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 13",
        "image_url": "/static/images/tshirt_13.jpg",
        "description": "A stylish brown t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 14",
        "image_url": "/static/images/tshirt_14.jpg",
        "description": "A comfortable beige t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 15",
        "image_url": "/static/images/tshirt_15.jpg",
        "description": "A trendy teal t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 16",
        "image_url": "/static/images/tshirt_16.jpg",
        "description": "A stylish maroon t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 17",
        "image_url": "/static/images/tshirt_17.jpg",
        "description": "A comfortable navy t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 18",
        "image_url": "/static/images/tshirt_18.jpg",
        "description": "A trendy olive t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 19",
        "image_url": "/static/images/tshirt_19.jpg",
        "description": "A stylish coral t-shirt.",
        "likes": randint(0, 100),
        "price": 24.99,
    },
    {
        "name": "T-shirt 20",
        "image_url": "/static/images/tshirt_20.jpg",
        "description": "A comfortable lavender t-shirt.",
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
    pass


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
