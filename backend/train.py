#code to train your own model with your package versions to avoid conflicts

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df  = pd.read_csv('./Crop_recommendation.csv') # Download your data from kaagle

X = df[['N', 'P', 'K', 'rainfall', 'humidity', 'temperature', 'ph']] 
y = df['label'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

best_model = RandomForestClassifier()
best_model.fit(X, y)

import joblib
joblib.dump(best_model, 'crop_recommendation_model.pkl')
