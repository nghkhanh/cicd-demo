import pytest
import os
from src.train_model import train_and_save_model
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

class TestModelTraining:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        os.makedirs("models", exist_ok=True)

        yield
    
    def test_train_model_success(self):
        accuracy = train_and_save_model()
        assert accuracy is not None
        assert isinstance(accuracy, (float, np.floating))
        assert 0 <= accuracy <= 1

    def test_model_accuracy_threshold(self):
        accuracy = train_and_save_model()
        assert accuracy >= 0.9, f"Model accuracy {accuracy: .2f%} is below 90% threshold"

    def test_model_accuracy_threshould(self):
        train_and_save_model()
        assert os.path.exists("models/iris_model.pkl")
        assert os.path.getsize("models/iris_model.pkl") > 0

    def test_model_can_be_loaded(self):
        train_and_save_model()
        with open("models/iris_model.pkl", "rb") as f:
            model = pickle.load(f)
        assert isinstance(model, RandomForestClassifier)
        assert hasattr(model, "predict")
        assert hasattr(model, "predict_proba")


if __name__ == "__main__":
    pytest.main([__file__, "v"])
