from flask import Flask, jsonify, request
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]

model = None


def train_model():
    global model
    california = fetch_california_housing(as_frame=True)
    df = california.frame

    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)


train_model()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expected JSON input example:
    {
        "MedInc": 3.5,
        "HouseAge": 20,
        "AveRooms": 5.0,
        "AveBedrms": 1.0,
        "Population": 1000,
        "AveOccup": 3.0,
        "Latitude": 37.8,
        "Longitude": -122.2
    }
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    missing = [feature for feature in FEATURES if feature not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        input_values = [float(data[feature]) for feature in FEATURES]
    except (TypeError, ValueError):
        return jsonify({"error": "All feature values must be numbers"}), 400

    prediction = model.predict([input_values])[0]
    return jsonify({
        "prediction": round(float(prediction), 4),
        "features": dict(zip(FEATURES, input_values))
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
