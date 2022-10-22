import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


def encode_labels(y_train, y_val, y_test):
    # Instantiate label encoder
    label_encoder = LabelEncoder()

    # fit to the training data
    label_encoder = label_encoder.fit(y_train)
    classes = list(label_encoder.classes_)
    print(f"Classes: {classes}")

    # convert labels to tokens
    print(f"y_train[0]: {y_train[0]}")
    _y_train = label_encoder.transform(y_train)
    _y_val = label_encoder.transform(y_val)
    _y_test = label_encoder.transform(y_test)
    print(f"y_train[0] as token: {_y_train[0]}")

    # get class weights
    counts = np.bincount(_y_train)
    class_weights = {i: 1.0/count for i, count in enumerate(counts)}
    return _y_train, _y_val, _y_test, counts, class_weights, classes


def standardize(X_train, X_val, X_test):

    # Set standardization to mean, std of training set (mean = 0, std = 1).
    X_scaler = StandardScaler().fit(X_train)

    # Apply scaler to all input data (not output data)
    _X_train = X_scaler.transform(X_train)
    _X_val = X_scaler.transform(X_val)
    _X_test = X_scaler.transform(X_test)

    return _X_train, _X_val, _X_test
