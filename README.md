# 🛡️ Blockchain IoT Security System — Setup Guide

**Smart Web Attack Detection System using Multi-Model Deep Learning + Blockchain AES Encryption**

---

## ✅ Prerequisites (Install these first)

| Software | Download Link |
|----------|--------------|
| Python 3.6.2 | https://www.python.org/downloads/release/python-362/ |
| MySQL Server 8.0 | https://dev.mysql.com/downloads/installer/ |
| MySQL Workbench | https://dev.mysql.com/downloads/workbench/ |

---

## 🚀 Step-by-Step Commands (Fresh Setup)

### STEP 1 — Open PowerShell and navigate to the project folder

```powershell
cd "C:\Major project\Major project\Blockchain A Game Changer for Securing IoT Data\blackchine_project"
```

---

### STEP 2 — Create a Python virtual environment

```powershell
python -m venv venv
```

---

### STEP 3 — Activate the virtual environment

```powershell
.\venv\Scripts\Activate
```

> ✅ You should see **(venv)** appear at the start of the prompt

---

### STEP 4 — Install all required packages

```powershell
pip install Django==3.2.25
pip install PyMySQL==1.0.2
pip install cryptography
pip install scikit-learn
pip install numpy
pip install scipy
```

OR install everything in one command using the requirements file:

```powershell
pip install -r requirements.txt
```

---

### STEP 5 — Set up MySQL Database

Open **MySQL Workbench** or **MySQL Command Line** and run:

```sql
CREATE DATABASE blockchain_iot;
```

> ⚠️ Make sure MySQL is running on port **3306** with:
> - Username: `root`
> - Password: `1278`
>
> If your password is different, update it in `blackchine_project/settings.py` → `DATABASES` section.

---

### STEP 6 — Run database migrations (creates all tables)

```powershell
python manage.py makemigrations
python manage.py migrate
```

> ✅ You should see: `Applying user.0001_initial... OK`

---

### STEP 7 — Start the development server

```powershell
python manage.py runserver
```

> ✅ You should see in the terminal:
> ```
> ========================================================
>   IoT ML Security Engine — Training classifiers...
> ========================================================
> [*] Training CNN model on IoT attack dataset...
> [*] Training LSTM model on IoT attack dataset...
> [*] Training MRN model on IoT attack dataset...
> [OK] Ensemble ready. Server is protected.
> ========================================================
> Starting development server at http://127.0.0.1:8000/
> ```

---

### STEP 8 — Open the website in your browser

```
http://127.0.0.1:8000
```

---

## 🌐 All Pages

| Page | URL | What it does |
|------|-----|-------------|
| Home / Login | `http://127.0.0.1:8000` | User login page |
| Register | `http://127.0.0.1:8000/user/register` | Create new account |
| Upload IoT Data | `http://127.0.0.1:8000/user/userpage` | Upload CSV files (ML scans here) |
| View Data | `http://127.0.0.1:8000/user/viewdata` | Send OTP & view uploaded files |
| Analytics | `http://127.0.0.1:8000/graphical_page` | Graphical charts of upload locations |
| Admin Login | `http://127.0.0.1:8000/admin-login` | Admin portal login |
| Admin Dashboard | `http://127.0.0.1:8000/admin-dashboard` | View all users, files, attack logs |

---

## 🔐 Admin Credentials

```
Username : admin
Password : admin123
```

---

## 🧪 Test Files for Demo

| File | What it tests |
|------|--------------|
| `attack_cnn_xss.csv` | XSS attack — triggers **CNN** model (95%) |
| `attack_lstm_sqli.csv` | SQL Injection — triggers **LSTM** model (98%) |
| `attack_mrn_pathtraversal.csv` | Path Traversal — triggers **MRN** model (99%) |
| `sample_iot_data.csv` | Clean data — uploads successfully and encrypts |

---

## 🔁 How to Run Again (After First Setup)

Every time you want to run the project again, just do:

```powershell
cd "C:\Major project\Major project\Blockchain A Game Changer for Securing IoT Data\blackchine_project"
.\venv\Scripts\Activate
python manage.py runserver
```

---

## ❗ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `No module named 'django'` | Run `.\venv\Scripts\Activate` first |
| `No module named 'sklearn'` | Run `pip install scikit-learn` |
| `Can't connect to MySQL` | Start MySQL service in Windows Services |
| `Table doesn't exist` | Run `python manage.py migrate` |
| `SMTPAuthenticationError` | OTP will show on screen instead (demo mode works) |

---

## 📁 Key Files Reference

```
blackchine_project/
├── manage.py                     ← Run server from here
├── requirements.txt              ← All Python packages
├── blackchine_project/
│   ├── settings.py               ← Database config (change password here)
│   └── emailsetting.py           ← Gmail SMTP config
├── user/
│   ├── ml_engine.py              ← CNN + LSTM + MRN ML models
│   ├── views.py                  ← All page logic
│   └── models.py                 ← Database models
├── attack_cnn_xss.csv            ← Demo: XSS attack file
├── attack_lstm_sqli.csv          ← Demo: SQL injection file
└── attack_mrn_pathtraversal.csv  ← Demo: Path traversal file
```
