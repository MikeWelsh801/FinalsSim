import numpy as np
import random
import torch as torch
import LoadFile as Load
from SplitData import train_val_test_split
import preprocess as pr
import NNTrainUtil as Train
import Evaluate as Eval
import json
import matplotlib.pyplot as plt
import Plot as Pl
import TorchNNUtil as Util
from torch.optim import Adam
import torch.nn.functional as F
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Set seed, so we get same data every time
SEED = 1234
LEARNING_RATE = 1e-2
np.random.seed(SEED)
random.seed(SEED)

# call loading function and plot
df, X, y = Load.load_from_file("./NN Stuff/NBA_Training_Data.csv")
# Load.plot(X, y, "Games by Fg%")

# split up the data into training, test, validation sets
TRAIN_SIZE = 0.7
X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(X, y, TRAIN_SIZE)
print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"X_val: {X_val.shape}, y_train: {y_val.shape}")
print(f"X_test: {X_test.shape}, y_train: {y_test.shape}")
# print(f"Sample point: {X_train[0]} -> {y_train[0]}")
print()

# -----Preprocessing--------------

# Convert output labels to tokens
y_train, y_val, y_test, counts, class_weights, classes = pr.encode_labels(y_train, y_val, y_test)
print(f"counts: {counts}\nweights: {class_weights}")
print()

# capture mean and std for normalizing samples
means = np.mean(X_train, axis=0)
stds = np.std(X_train, axis=0)

# Standardize all input data and check that mean ~ 0 and std ~ 1
X_train, X_val, X_test = pr.standardize(X_train, X_val, X_test)
print(f"X_test[0]: mean: {np.mean(X_test[:, 0], axis=0):.1f}, std: {np.std(X_test[:, 0], axis=0):.1f}")
print(f"X_test[1]: mean: {np.mean(X_test[:, 1], axis=0):.1f}, std: {np.std(X_test[:, 1], axis=0):.1f}")

# Set seed for reproducibility
torch.manual_seed(SEED)

# set up layers and initialize linear model
INPUT_DIM = X_train.shape[1]  # 84-dimensional
HIDDEN_DIM = 100
NUM_CLASSES = len(classes)  # 2 classes

print()
print("**** Training Network ****")
print()

# Convert tensors to NumPy arrays
# X_train = X_train.numpy()
# y_train = y_train.numpy()
# X_val = X_val.numpy()
# y_val = y_val.numpy()
# X_test = X_test.numpy()
# y_test = y_test.numpy()

# # Initialize weights
# W1, b1, W2, b2 = Train.initialize_weights(INPUT_DIM, HIDDEN_DIM, NUM_CLASSES)
#
# # Training Loop
# for epoch_num in range(1000):
#
#     # complete forward pass
#     y_hat, a1 = Train.forward_pass(X_train, W1, b1, W2, b2)
#
#     # update loss
#     loss = Train.compute_loss(y_hat, y_train)
#
#     # update progress
#     if epoch_num % 100 == 0:
#         y_pred = np.argmax(y_hat, axis=1)
#         accuracy = np.mean(np.equal(y_train, y_pred))
#         print(f"Epoch: {epoch_num}, loss: {loss:.3f}, accuracy: {accuracy:.3f}")
#
#     # Get gradients
#     dW1, dW2, db1, db2 = Train.compute_grads(y_hat, y_train, X_train, a1, W2)
#
#     # Update Weights
#     W1 -= LEARNING_RATE * dW1
#     b1 -= LEARNING_RATE * db1
#     W2 -= LEARNING_RATE * dW2
#     b1 -= LEARNING_RATE * db1
#
#
# # Evaluate with a forward pass call on trained weights
# class MLPFromScratch:
#     def predict(self, x):
#         return Train.predict(x, W1=W1, W2=W2, b1=b1, b2=b2)
#
#
# model = MLPFromScratch()
# y_prob = model.predict(X_test)
# y_pred = np.argmax(y_prob, axis=1)
# performance = Eval.get_metrics(y_true=y_test, y_pred=y_pred, classes=classes)
# print(json.dumps(performance, indent=2))

# Visualize the decision boundary
# plt.figure(figsize=(12, 5))
# plt.subplot(1, 2, 1)
# plt.title("Train")
# Pl.plot_multiclass_decision_boundary_numpy(model=model, X=X_train, y=y_train)
# plt.subplot(1, 2, 2)
# plt.title("Test")
# Pl.plot_multiclass_decision_boundary_numpy(model=model, X=X_test, y=y_test)
# plt.show()

# Drop 10% of weights each pass
DROPOUT_P = 0.15

# Initialize model
model = Util.MLP(input_dim=INPUT_DIM, hidden_dim=HIDDEN_DIM, dropout_p=DROPOUT_P, num_classes=NUM_CLASSES)
print(model.named_parameters)

# Define loss
loss_fn = Util.loss_function(class_weights=class_weights)

optimizer = Adam(model.parameters(), lr=LEARNING_RATE)

# Convert data to tensors
X_train = torch.Tensor(X_train)
y_train = torch.LongTensor(y_train)
X_val = torch.Tensor(X_val)
y_val = torch.LongTensor(y_val)
X_test = torch.Tensor(X_test)
y_test = torch.LongTensor(y_test)

# Training
NUM_EPOCHS = 200

Util.train(model=model, X_train=X_train, y_train=y_train,
           num_epochs=NUM_EPOCHS, optimizer=optimizer, loss_fn=loss_fn)

# predictions
y_prob = F.softmax(model(X_test), dim=1)
y_pred = y_prob.max(dim=1)[1]

# performance
performance = Eval.get_metrics(y_true=y_test, y_pred=y_pred, classes=classes)
print(json.dumps(performance, indent=2))

# Inputs for inference
predDF, X_infer, y_null = Load.load_from_file(
    "./NN Stuff/BOSTON_FINALS.csv")

# Standardize
X_infer -= means
X_infer /= stds


y_infer = F.softmax(model(torch.Tensor(X_infer)), dim=1)
print(y_infer)
prob, _class = y_infer.max(dim=1)
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
label = label_encoder.inverse_transform(_class.detach().numpy())[0]

print(f"The probability that Boston will win at home is {y_infer.detach().numpy()[0][1]*100.0}%")

# Inputs for inference
predDF2, X_inferB, y_null2 = Load.load_from_file(
    "./NN Stuff/2022_NBA_FINALS_DATA.csv")

# Standardize
X_inferB -= means
X_inferB /= stds

y_inferB = F.softmax(model(torch.Tensor(X_inferB)), dim=1)
prob2, _class2 = y_inferB.max(dim=1)
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
label2 = label_encoder.inverse_transform(_class2.detach().numpy())[0]
print(y_inferB)


print(f"The probability that Golden Sate will win at home is {y_inferB.detach().numpy()[0][1]*100.0}%")
