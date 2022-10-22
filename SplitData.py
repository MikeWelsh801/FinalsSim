from sklearn.model_selection import train_test_split


# Splits up the data (train, val, test sets)
# given X, y and training size
def train_val_test_split(X, y, train_size):
    X_train, X_, y_train, y_ = train_test_split(X, y, train_size=train_size, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_, y_, train_size=0.5, stratify=y_)
    return X_train, X_val, X_test, y_train, y_val, y_test