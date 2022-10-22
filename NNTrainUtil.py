import numpy as np
import random

SEED = 1234
np.random.seed(SEED)
random.seed(SEED)


def initialize_weights(input_dim, hidden_dim, num_classes):
    #  Initialize firs layer weights w/ zero bias
    W1 = 0.01 * np.random.randn(input_dim, hidden_dim)
    b1 = np.zeros((1, hidden_dim))
    W2 = 0.01 * np.random.randn(hidden_dim, num_classes)
    b2 = np.zeros((1, num_classes))
    return W1, b1, W2, b2


def forward_pass(X_train, W1, b1, W2, b2):
    # z1 = X * W1 add bias -- NX2 * 2X100 + 1X100 = NX100
    z1 = np.dot(X_train, W1) + b1

    # first activation function ReLU max(y or zero)
    a1 = np.maximum(0, z1)

    # z2 = logits = a1 * W2 add bias -- NX100 * 100X3 + 1X3 = NX3
    logits = np.dot(a1, W2) + b2

    # normalize via softmax e^z2_i/sum(e^z2) (interpret as probabilities)
    exp = np.exp(logits)
    y_hat = exp / np.sum(exp, axis=1, keepdims=True)
    return y_hat, a1


def compute_loss(y_hat, y_train):
    # Calculate loss
    correct_class_logprobs = -np.log(y_hat[range(len(y_hat)), y_train])
    loss = np.sum(correct_class_logprobs) / len(y_train)
    return loss


def compute_grads(y_hat, y_train, X_train, a1, W2):
    #  Compute dJ/dW2 w/ bias grad
    dscores = y_hat
    dscores[range(len(y_hat)), y_train] -= 1
    dscores /= len(y_train)
    dW2 = np.dot(a1.T, dscores)
    db2 = np.sum(dscores, axis=0, keepdims=True)

    # compute dJ/dW1 w bias grad
    dhidden = np.dot(dscores, W2.T)
    dhidden[a1 <= 0] = 0
    dW1 = np.dot(X_train.T, dhidden)
    db1 = np.sum(dhidden, axis=0, keepdims=True)
    return dW1, dW2, db1, db2


def predict(X_train, W1, b1, W2, b2):
    # z1 = X * W1 add bias -- NX2 * 2X100 + 1X100 = NX100
    z1 = np.dot(X_train, W1) + b1

    # first activation function ReLU max(y or zero)
    a1 = np.maximum(0, z1)

    # z2 = logits = a1 * W2 add bias -- NX100 * 100X3 + 1X3 = NX3
    logits = np.dot(a1, W2) + b2

    # normalize via softmax e^z2_i/sum(e^z2) (interpret as probabilities)
    exp = np.exp(logits)
    y_hat = exp / np.sum(exp, axis=1, keepdims=True)
    return y_hat
