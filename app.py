from flask import Flask, jsonify, request

app = Flask(__name__)

products = []

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask API"})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    product = {
        "id": len(products) + 1,
        "name": data.get("name"),
        "price": data.get("price"),
        "category": data.get("category")
    }

    products.append(product)
    return jsonify({"message": "Product added successfully", "product": product}), 201


if __name__ == '__main__':
    app.run(debug=True)
