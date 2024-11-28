import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def preprocess(self, df):
        # Assume last column is target
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        # Handle categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

        # Label encode categorical columns
        for col in categorical_cols:
            X[col] = self.label_encoder.fit_transform(X[col])

        # Scale numerical columns
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])

        # Encode target
        y = self.label_encoder.fit_transform(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        return X_train, X_test, y_train, y_test
