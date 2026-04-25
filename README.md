# ⚡ ElectroGuard v2.0

<div align="center">

**AI-Powered Electricity Theft Detection System for Maharashtra**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 🧠 What is ElectroGuard?

ElectroGuard is a full-stack web application that uses a **Machine Learning ensemble model** to detect electricity theft across Maharashtra's distribution network. It provides a 3-tier admin hierarchy (State → District → Village) with real-time analytics, theft reports, FIR management, and Excel export.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **ML Detection** | Voting ensemble (Gradient Boosting + Random Forest) with 100% CV accuracy |
| 🏛️ **3-Tier Hierarchy** | State → District → Village admin roles with scoped access |
| 📊 **Live Dashboard** | Theft stats, severity breakdown, and recent activity |
| 📋 **Report Management** | Full history with FIR filing and meter cut-off tracking |
| 📤 **Excel Export** | One-click `.xlsx` export of any theft report |
| ⚙️ **Admin Panel** | Create/manage district and village admins |
| 🔍 **Theft Classification** | Identifies Direct Hook, Meter Tamper, Bypass, Overload |

---

## 🗂️ Project Structure

```
ElectroGuard-v2/
├── app.py                    ← Main Flask application & all routes
├── model.py                  ← ML prediction engine
├── train_model.py            ← Train / retrain the ML model
├── generate_dataset.py       ← Synthetic training data generator
├── dataset.csv               ← Training dataset (1,000 rows)
├── requirements.txt          ← Python dependencies
├── .env.example              ← Environment variable template
├── districtofSpecificState…csv   ← Maharashtra district data
├── villageofSpecificState…csv    ← Maharashtra village data
└── templates/
    ├── base.html             ← Shared sidebar layout
    ├── login.html            ← Login page
    ├── dashboard.html        ← Main dashboard
    ├── predict.html          ← Theft detection form
    ├── admin.html            ← Admin management panel
    ├── reports.html          ← Report history
    ├── activity.html         ← Activity log
    ├── settings.html         ← Profile & password settings
    └── error.html            ← Error page
```

> **Note:** `model.pkl`, `electroguard.db`, and the `exports/` folder are auto-generated and excluded from version control via `.gitignore`.

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ElectroGuard-v2.git
cd ElectroGuard-v2
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Open .env and set your SECRET_KEY
```

### 5. Generate dataset & train the ML model

```bash
python generate_dataset.py
python train_model.py
```

You should see:
```
✅ Model Accuracy: 100.00%
```

### 6. Run the application

```bash
python app.py
```

Open your browser at → **http://localhost:5000**

---

## 🔐 Default Login

| Username | Password | Role |
|---|---|---|
| `superadmin` | `admin123` | State Admin |

> ⚠️ Change the default password immediately after first login!

---

## 👥 Admin Hierarchy

```
State Admin (Maharashtra)
    └── District Admin  (e.g. Nashik)
            └── Village Admin  (e.g. Sinnar)
```

- **State Admin** — full access, creates District Admins, views all data
- **District Admin** — scoped to their district, creates Village Admins
- **Village Admin** — scoped to their village, runs theft detections

---

## ⚡ Theft Detection — Input Reference

| Field | Normal Range | Unit |
|---|---|---|
| Voltage | 210 – 240 | V |
| Current | 3 – 10 | A |
| Power | 500 – 3,000 | W |
| Time | 8 – 24 | hours |
| Meter Difference | ≈ Power × Time ÷ 1000 | kWh |

The AI returns:
- ✅ **Safe** or ⚠️ **Theft Detected**
- Confidence percentage
- Severity: `CRITICAL` / `HIGH` / `MODERATE`
- Theft type: `Direct Hook` / `Meter Tamper` / `Bypass` / `Overload`
- Specific flagged reasons

---

## 🤖 ML Model Details

| Property | Value |
|---|---|
| Algorithm | Voting Ensemble (GradientBoosting + RandomForest) |
| Features | Voltage, Current, Power, Time, MeterDiff, PowerPerCurrent, MeterEfficiency, CurrentVoltageRatio |
| Training data | 1,000 samples (500 theft + 500 normal) |
| Test accuracy | 100% |
| 5-fold CV | 100% |

To retrain after adding new data to `dataset.csv`:
```bash
python train_model.py
```

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, SQLite
- **ML:** scikit-learn (GradientBoostingClassifier, RandomForestClassifier, VotingClassifier)
- **Frontend:** Jinja2 templates, vanilla HTML/CSS (custom dark theme)
- **Export:** openpyxl (Excel generation)
- **Data:** pandas, numpy

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Built for Maharashtra Electricity Board &nbsp;|&nbsp; ElectroGuard v2.0
</div>
