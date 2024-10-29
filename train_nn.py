# Save as train_nn.py
import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class TitanicNet(nn.Module):
    """A simple feed-forward neural network for binary classification."""

    def __init__(self):
        super(TitanicNet, self).__init__()
        self.fc1 = nn.Linear(7, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x):
        """Defines the forward pass of the network."""
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

def train(train_path, val_path, epochs, learning_rate):
    """
    Train the TitanicNet model on provided training and validation data.

    Parameters:
    - train_path (str): Path to the training data (.npz file).
    - val_path (str): Path to the validation data (.npz file).
    - epochs (int): Number of training epochs.
    - learning_rate (float): Learning rate for the optimizer.
    """
    # Load data
    train_data = np.load(train_path)
    val_data = np.load(val_path)
    X_train, y_train = train_data['X_train'], train_data['y_train']
    X_val, y_val = val_data['X_val'], val_data['y_val']
    
    # Convert to torch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_val = torch.tensor(X_val, dtype=torch.float32)
    y_val = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)
    
    # Initialize model, loss, and optimizer
    model = TitanicNet()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        
        # Validation
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val)
            val_loss = criterion(val_outputs, y_val)
        
        if (epoch + 1) % 1000 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, Val Loss: {val_loss.item():.4f}", flush=True)

    
    # Save model
    model_output_path = "/opt/ml/model/nn_model.pth" if os.path.exists("/opt/ml/model") else "nn_model.pth"
    torch.save(model.state_dict(), model_output_path)
    print(f"Model saved to {model_output_path}")

if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description="Train TitanicNet on provided data")
    parser.add_argument('--train', type=str, required=True, help="Path to training data (.npz file)")
    parser.add_argument('--val', type=str, required=True, help="Path to validation data (.npz file)")
    parser.add_argument('--epochs', type=int, default=10, help="Number of training epochs")
    parser.add_argument('--learning_rate', type=float, default=0.001, help="Learning rate for optimizer")
    
    args = parser.parse_args()
    train(args.train, args.val, args.epochs, args.learning_rate)
