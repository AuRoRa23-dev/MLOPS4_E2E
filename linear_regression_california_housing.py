import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def main():
    print("Loading California housing dataset...")
    california = fetch_california_housing(as_frame=True)
    df = california.frame

    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nLinear Regression Model Trained")
    print(f"RMSE: {rmse:.4f}")
    print(f"R^2 Score: {r2:.4f}")
    print("\nSample predictions:")
    for actual, predicted in zip(y_test.head(5), predictions[:5]):
        print(f"Actual: {actual:.2f} | Predicted: {predicted:.2f}")


if __name__ == "__main__":
    main()
