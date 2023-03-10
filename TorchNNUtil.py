from torch import nn
import torch.nn.functional as F
from torch.optim import Adam
import torch
from torch.nn import init


class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, dropout_p, num_classes):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout_p)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def int_weights(self):
        init.xavier_normal(self.fc1.weight, gain=init.calculate_gain("relu"))

    def forward(self, x_in):
        z = F.relu(self.fc1(x_in))
        z = self.dropout(z)
        z = self.fc2(z)
        return z


def loss_function(class_weights):
    class_weights_tensor = torch.Tensor(list(class_weights.values()))
    loss_fn = nn.CrossEntropyLoss(weight=class_weights_tensor)
    return loss_fn


def accuracy_fn(y_pred, y_true):
    """Returns the accuracy of a model"""
    n_correct = torch.eq(y_pred, y_true).sum().item()
    accuracy = (n_correct / len(y_pred)) * 100
    return accuracy


def train(model, X_train, y_train, num_epochs, optimizer, loss_fn):
    for epoch in range(num_epochs):
        # Forward pass
        y_pred = model(X_train)

        # Loss
        loss = loss_fn(y_pred, y_train)

        # Zero out gradients
        optimizer.zero_grad()

        # Backward pass
        loss.backward()

        # Update weights
        optimizer.step()

        if epoch % 10 == 0:
            predictions = y_pred.max(dim=1)[1]
            accuracy = accuracy_fn(y_pred=predictions, y_true=y_train)
            # print(f"Epoch: {epoch} | loss: {loss:.2f}, accuracy: {accuracy:.1f}")
