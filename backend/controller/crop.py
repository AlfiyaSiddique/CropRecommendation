from flask import request, jsonify
import numpy as np
import joblib
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import requests
from bs4 import BeautifulSoup

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

crop_recommend_model = joblib.load('modules/crop_recommendation_model.pkl')
crop_disease_detect_model_path = 'modules/crop_disease_model.pkl'

def predictCrop():
    try:
        data = request.get_json()

        features = np.array([
            data['N'],
            data['P'],
            data['K'],
            data['rainfall'],
            data['ph'],
            data['humidity'],
            data['temperature']
        ]).reshape(1, -1)  

        prediction = crop_recommend_model.predict(features)

        return jsonify({'prediction': {"crop": prediction[0]}})
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



crop_disease_detect_model = CropDiseaseModel()
crop_disease_detect_model.load_state_dict(torch.load("modules/crop_disease_model.pkl"))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
crop_disease_detect_model.to(device)
crop_disease_detect_model.eval()

transforms = transforms.Compose([
    transforms.Resize((64,64)),
    transforms.RandomRotation(10),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
])


CLASS_NAMES = ['coffee', 'coffee_Disease', 'coffee_Disease_miner', 'coffee_Disease_rust', 'coffee_healthy', 'cotton', 'cotton_Disease', 'cotton_Disease_Aphids edited', 'cotton_Disease_Army worm edited', 'cotton_Disease_Bacterial Blight edited', 'cotton_Disease_Powdery Mildew Edited', 'cotton_Disease_Target spot edited', 'cotton_Healthy', 'jute', 'jute_Disease', 'jute_Disease_Cescospora Leaf Spot', 'jute_Disease_Golden Mosaic', 'jute_Healthy', 'rice', 'rice_Disease', 'rice_Disease_Bacterial leaf blight', 'rice_Disease_Brown spot', 'rice_Disease_Leaf smut', 'rice_Healthy', 'sugarcane', 'sugarcane_Disease', 'sugarcane_Disease_Mosaic', 'sugarcane_Disease_RedRot', 'sugarcane_Disease_Rust', 'sugarcane_Disease_Yellow', 'sugarcane_Healthy', 'wheat', 'wheat_Disease', 'wheat_Disease_septoria', 'wheat_Disease_stripe_rust', 'wheat_Healthy']

def scrape_solution(disease_name):
    try:
        search_url = f"https://www.google.com/search?q={disease_name.replace(' ', '+')}+treatment"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")

        if result:
            return result.text
        else:
            return "Solution not found"

    except Exception as e:
        return f"Error fetching solution: {str(e)}"

def detectDisease():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files["image"]
    image = Image.open(image_file).convert("RGB")
    image = transforms(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = crop_disease_detect_model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)  # Convert raw scores to probabilities
        top_prob, predicted = torch.max(probabilities, 1)  # Get highest probability class
        predicted_class_idx = predicted.item()

        print("Predicted class index:", predicted_class_idx)  # Debugging
        print("Top Probability:", top_prob.item())  # Check confidence level

        disease_name = CLASS_NAMES[predicted_class_idx]

    # Extract disease name
    if "disease" in disease_name.lower():
        disease_only = disease_name.split("_")[-1]
    else:
        disease_only = "healthy"

    if disease_only == "healthy":
        return jsonify({"status": "healthy", "message": "No disease detected"})

    solution = scrape_solution(disease_only)

    return jsonify({
        "status": "disease_detected",
        "disease": disease_only,
        "solution": solution
    }), 200

    print("1")
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files["image"]
    image = Image.open(image_file).convert("RGB")
    image = transforms(image).unsqueeze(0).to(device)

    print("2")
    with torch.no_grad():
        print("3")
        output = crop_disease_detect_model(image)
        _, predicted = torch.max(output, 1)
        predicted_class_idx = predicted.item()
        print("Predicted class index:", predicted_class_idx)
        disease_name = CLASS_NAMES[predicted.item()]

    if disease_name.lower().find("healthy") != -1:
        return jsonify({"status": "healthy", "message": "No disease detected"})
    
    solution = scrape_solution(disease_name)

    return jsonify({"status": "disease_detected", "disease": disease_name, "solution": solution}), 200
