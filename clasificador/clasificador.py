from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

class SVMClassifier:
    def __init__(self, file_path, kernel='linear', C=1.0):
        self.file_path = file_path
        self.model = svm.SVC(kernel=kernel, C=C)
        self.dataset = self.load_dataset()
        self.label_encoder = LabelEncoder()
        self.vectorizer = TfidfVectorizer()

    def load_dataset(self):
        return pd.read_csv(self.file_path, delimiter='|')

    def preprocess_data(self):
        X = self.dataset['text']
        y_str = self.dataset['category']

        y = self.label_encoder.fit_transform(y_str)
        X_vectorized = self.vectorizer.fit_transform(X)

        return X_vectorized, y

    def train(self):
        X, y = self.preprocess_data()
        self.model.fit(X, y)

    def predict(self):
        X, _ = self.preprocess_data()
        return self.model.predict(X)

    def evaluate(self):
        X, y_true = self.preprocess_data()
        y_pred = self.predict()
        accuracy = accuracy_score(y_true, y_pred)
        return accuracy
