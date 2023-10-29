from sklearn import svm
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer


class SVMClassifier:
    def __init__(self, file_path, kernel='linear', c=1.0):
        self.file_path = file_path
        self.model = svm.SVC(kernel=kernel, C=c)
        self.dataset = self.load_dataset()
        self.label_encoder = LabelEncoder()
        self.vectorizer = TfidfVectorizer()

    def load_dataset(self):
        dataset = pd.read_csv(self.file_path, delimiter='|')
        dataset = dataset.dropna()
        return dataset

    def preprocess_data(self):
        x = self.dataset['text']
        y_str = self.dataset['category']

        y = self.label_encoder.fit_transform(y_str)
        x_vectorized = self.vectorizer.fit_transform(x)

        return x_vectorized, y

    def train(self):
        x, y = self.preprocess_data()
        self.model.fit(x, y)

    def predict(self):
        x, _ = self.preprocess_data()
        return self.model.predict(x)

    def evaluate(self):
        x, y_true = self.preprocess_data()
        y_pred = self.predict()
        accuracy = accuracy_score(y_true, y_pred)
        return accuracy
