TEST DATA — Blockchain IoT Security System
==========================================

FOLDER STRUCTURE:
-----------------

📁 attack_files/         ← Upload these to TRIGGER the ML security system
│
├── attack_cnn_xss.csv              → Cross-Site Scripting (XSS)
│                                     Triggers: CNN Model (95% confidence)
│
├── attack_lstm_sqli.csv            → SQL Injection attack
│                                     Triggers: LSTM Model (98% confidence)
│
└── attack_mrn_pathtraversal.csv    → Path Traversal + Command Injection
                                      Triggers: MRN Model (99% confidence)

📁 clean_files/          ← Upload these to test NORMAL successful upload
│
└── sample_iot_data.csv             → Normal IoT sensor data
                                      Result: Uploads, encrypts, and stores fine

HOW TO USE:
-----------
1. Login to the website at http://127.0.0.1:8000
2. Go to "Upload Data" page
3. Upload any file from attack_files/ → System blocks it with ML popup
4. Upload sample_iot_data.csv        → System encrypts and stores it
5. Go to Admin Dashboard to see all logs and download encrypted files
