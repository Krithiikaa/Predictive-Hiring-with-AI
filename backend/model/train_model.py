import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pickle
import os

# ✅ Step 1: Load dataset using full path
df = pd.read_csv('C:/Users/ASUS/Desktop/predictive-hiring-app/dataset/hiring_data.csv')

# ✅ Step 2: Drop columns not needed (if present)
df = df.drop(columns=['Name', 'Email'], errors='ignore')

# ✅ Step 3: Fill missing values
df.fillna('Unknown', inplace=True)

# ✅ Step 4: Encode categorical features
le = LabelEncoder()
for col in df.select_dtypes(include='object'):
    df[col] = le.fit_transform(df[col])

# ✅ Step 5: Define features and target
target_column = 'Success in Hiring Process'  # ✅ Correct

 # Change this if your column is named differently
X = df.drop(columns=[target_column])
y = df[target_column]

# ✅ Step 6: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("🧠 Model Training Columns:")
print(X.columns)

# ✅ Step 7: Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ✅ Step 8: Evaluate model
y_pred = model.predict(X_test)
print("🔍 Model Performance:\n")
print(classification_report(y_test, y_pred))

# ✅ Step 9: Save model
os.makedirs('model', exist_ok=True)
with open('model/predictive_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully!")
