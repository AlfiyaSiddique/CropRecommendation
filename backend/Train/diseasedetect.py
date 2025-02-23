import torch
import torch.nn as nn
import torch.optim as optim

import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
from torchvision.datasets import DatasetFolder
from PIL import Image
import os

class CropDiseaseModel(nn.Module):
    def __init__(self):
        super(CropDiseaseModel, self).__init__()
        self.conv1 = nn.Conv2d(3,32,kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1= nn.Linear(16384, 128)
        self.fc2 = nn.Linear(128, 36)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(2,2)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.maxpool(self.relu(self.conv1(x)))
        x = self.maxpool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

transform = transforms.Compose([
    transforms.Resize((64,64)),
    transforms.RandomRotation(10),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
])

def find_classes(directory):
    """Recursively find all class labels (subdirectories)"""
    classes = []
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            class_path = os.path.relpath(os.path.join(root, d), directory)
            classes.append(class_path.replace(os.sep, "_"))
    classes = sorted(classes)
    class_to_idx = {"cls_name": i for i in enumerate(classes)}
    return classes, class_to_idx
    

def load_image(path):
    return Image.open(path).convert("RGB")

dataset_path = "/kaggle/input/indian-crop-disease-dataset/Crop Dataset" # change this to dataset path
classes, class_to_idx = find_classes(dataset_path)
print("Detected_Classes", classes)


dataset = DatasetFolder(
    root=dataset_path,
    loader=load_image,
    extensions=("jpg","jpeg","png"),
    transform=transform
)
dataset.classes = classes
dataset.class_to_idx = class_to_idx


train_loader = DataLoader(dataset, batch_size=16, shuffle=True)

print("Total Images loadeed:", len(dataset))
print("Classes detected", dataset.classes)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CropDiseaseModel().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


num_epochs = 10
for epoch in range(num_epochs):
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step() 
    
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "crop_disease_model.pkl")
print("Model training complete and saved!")
