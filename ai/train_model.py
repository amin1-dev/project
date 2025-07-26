import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load data
df = pd.read_csv('AI-based Career Recommendation System.csv')

# Preprocessing
# Encode categorical columns
label_cols = ['Education', 'Recommended_Career']
for col in label_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# Skills and Interests: simple encoding (count of skills/interests)
df['Skills_count'] = df['Skills'].apply(lambda x: len(str(x).split(';')))
df['Interests_count'] = df['Interests'].apply(lambda x: len(str(x).split(';')))

# Features and target
features = ['Age', 'Education', 'Skills_count', 'Interests_count']
X = df[features]
y = df['Recommended_Career']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Cross-validation
cv_scores = cross_val_score(clf, X_scaled, y, cv=5)
print(f'Cross-validation accuracy: {cv_scores.mean():.2f}')

# Save model and scaler
joblib.dump(clf, 'ai/model_rf.joblib')
joblib.dump(scaler, 'ai/scaler.joblib')
