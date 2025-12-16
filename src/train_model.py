import os
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
def train_and_save_model():
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=20, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy: .2f}")
    
    os.makedirs("models", exist_ok=True)
    with open("models/iris_model.kl", "wb") as f:
        pickle.dump(model, f)

    print("Model saved!")
    return accuracy

if __name__ == "__main__":
    train_and_save_model()

