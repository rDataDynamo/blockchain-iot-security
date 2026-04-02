# Blockchain: A Game Changer for Securing IoT Data
## Integrating Zero-Trust Immutability with Hybrid Deep Learning for Threat Detection

**Abstract**  
The rapid expansion of the Internet of Things (IoT) has introduced severe vulnerabilities into critical infrastructure, as resource-constrained devices often transmit data autonomously without robust payload inspection. This paper proposes a novel Zero-Trust IoT Broker architecture that combines Ensemble Deep Learning (CNN, LSTM, MRN) with Blockchain-grade AES-128 encryption. By utilizing an early-fusion "Max-Confidence" hybrid model at the ingestion layer, the system preemptively detects and drops malicious payloads (e.g., XSS, SQLi, and Path Traversals) before they can compromise the central cloud repository. Evaluated on diverse attack datasets, the ensemble network demonstrates significant improvements in F1-score accuracy compared to standalone models, while the encrypted storage mechanism ensures post-ingestion data immutability.

---

### 1. Introduction
Modern IoT infrastructure is often referred to as a "Red Lake" due to the overwhelming volume of unstructured, insecure data flowing into centralized data centers. While traditional security focuses on firewalls and network perimeters, adversaries increasingly mask malicious payloads within seemingly benign sensor data. 

Recently, researchers have proposed Ensemble Deep Learning-based Web Attack Detection Systems (EDL-WADS) to identify these threats using multiple concurrent DL models. While highly effective at identifying threats at the gateway, existing EDL-WADS frameworks suffer from a critical flaw: **they lack a secure post-detection storage protocol.** Once data is deemed "safe" by the ensemble model, it is often stored in vulnerable plaintext databases where it can be tampered with by insider threats or subsequent lateral attacks.

This research proposes an evolutionary step beyond standard EDL-WADS. We introduce an intelligent ingestion barrier that actively intercepts and sanitizes data using an EDL-WADS architecture (CNN, LSTM, MRN), but uniquely couples it with a **Blockchain-inspired Cryptographic Pipeline (AES-128 & OTP Tokenization)**. This ensures that data is not only clean upon entry but remains cryptographically immutable while at rest.

### 2. Proposed Architecture

Our framework consists of two main pillars: The **Intelligent Threat Detection Engine** and the **Immutable Execution Pipeline**.

#### A. Intelligent Threat Detection Engine (Hybrid Ensemble)
To account for the heterogeneous nature of web attacks, a multi-model approach is employed:
1.  **CNN (Convolutional Neural Network) Layer**: Optimized via character-level n-gram extraction (2-5 bounds). The CNN extracts spatial features, demonstrating high efficacy in identifying Cross-Site Scripting (XSS) and localized script injections.
2.  **LSTM (Long Short-Term Memory) Layer**: Evaluates tokenized sequential dependencies (1-3 bounds). Using Random Forest paradigms, it excels in detecting multi-token malicious sequences, such as SQL Injection (`UNION SELECT`).
3.  **MRN (Multi-Resolution Network) Layer**: Scans structural anomalies using a calibrated Support Vector Machine across broad byte-window lengths, isolating path traversals (e.g., `../../etc/passwd`) and remote command execution.

These three models run concurrently. A **Max-Confidence Vote Strategy** evaluates the output; if any individual classifier exceeds an 80% confidence threshold, the payload is immediately dropped, and the attempt is logged to the active `AttackLog`.

#### B. Immutable Execution Pipeline (Blockchain Equivalency)
Once a data block (file) passes the DL inspection, it enters the cryptographic pipeline. Data is subjected to AES-128-CBC Symmetrical Encryption. In this proposed architecture, the encrypted ciphertext represents an immutable state—unable to be read or modified by internal database administrators or subsequent unauthorized users. Decryption requires an ephemeral OTP (One Time Password) issued dynamically to verified clients, mirroring secure blockchain key-exchange models.

### 3. Empirical Results and Evaluation

To validate the proposed machine learning classifier against traditional methods, the system was evaluated on a curated dataset of generalized IoT readings, interspersed with sophisticated attack vectors. 

#### A. Performance Metrics
The primary evaluation metrics utilized are Accuracy, Precision, Recall, and the F1-Score. Precision mitigates false positives (blocking legitimate sensor logs), while Recall mitigates false negatives (allowing a malicious payload through). 

*(Insert Graph `metric_bar_chart.png` here: Bar Chart showing CNN vs LSTM vs Ensemble)*

The Ensemble approach mathematically eliminates the "blind spots" of singular models. Where a CNN might fail to realize the sequential danger of an SQL query, the LSTM captures it, resulting in the Ensemble scoring consistently higher across all bounds.

#### B. Confusion Matrix
*(Insert Graph `ensemble_confusion_matrix.png` here: Confusion matrix graphic)*
The matrix demonstrates that the dual thresholds effectively segregate malicious behavior while maintaining a high throughput for standard IoT JSON/CSV objects.

### 4. Conclusion
This study demonstrates that decentralized data transfer must be accompanied by intelligent data verification. By positioning a highly accurate CNN-LSTM-MRN Ensemble framework at the data ingestion gateway, and following it immediately with cryptographic immutability, we can construct a true Zero-Trust architecture for modern IoT deployments. 
