# ⚡ Carbon‑Smart EV Charging Scheduler

A **machine‑learning driven decision support system** that intelligently schedules Electric Vehicle (EV) charging by **balancing user urgency and carbon intensity of the power grid**. The project integrates **unsupervised learning, time‑series forecasting, and an interactive Streamlit dashboard**, backed by a production‑ready FastAPI service.

---

## 🚀 Project Motivation

With the rapid adoption of Electric Vehicles, **uncoordinated charging** can:

* Overload local power grids
* Increase peak‑hour emissions
* Waste opportunities to charge during cleaner energy windows

This project addresses the problem by:

* **Classifying EV users** based on urgency and energy needs
* **Predicting carbon intensity** for a given future timestamp
* **Advising carbon‑smart charging decisions** without compromising user requirements

---

## 🧠 System Architecture

```
Streamlit Frontend  ──▶  FastAPI Backend  ──▶  ML Models
        │                      │
        │                      ├─ User Clustering (K‑Means + Scaler)
        │                      ├─ Carbon Intensity Prediction (Regression)
        │                      └─ Temporal Feature Engineering
```

---

## 🧩 Key Features

### 🔹 Intelligent User Classification

* Uses **K‑Means clustering** to group users based on:

  * Arrival hour
  * Charging duration
  * Energy requirement
* Clusters are **mapped to meaningful labels**:

  * **Urgent User** (needs immediate charging)
  * **Flexible User** (can delay charging)

### 🔹 Carbon Intensity Forecasting

* Predicts grid carbon intensity for a **future timestamp**
* Automatically extracts temporal features:

  * Hour of day
  * Day of week
  * Month
* Supports **future‑aware prediction** (no data leakage)

### 🔹 Clean & Intuitive UI

* Built using **Streamlit** with custom CSS
* Visually distinguishes urgent vs flexible users
* Provides actionable feedback:

  * Low‑carbon window detected
  * Recommendation to delay charging

### 🔹 Production‑Ready Backend

* FastAPI with modular endpoints
* Hosted on **Render**
* Models loaded safely with environment‑agnostic paths

---

## 🛠️ Tech Stack

| Layer           | Technology                                   |
| --------------- | -------------------------------------------- |
| Frontend        | Streamlit + Custom CSS                       |
| Backend         | FastAPI + Uvicorn                            |
| ML              | Scikit‑learn, Pandas, NumPy                  |
| Models          | K‑Means, Linear Regression                   |
| Deployment      | Render (Backend), Streamlit Cloud (Frontend) |
| Version Control | Git & GitHub                                 |

---

## 📂 Project Structure

```
Carbon_Smart_Charging_Scheduler/
│
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── models/                  # Trained ML models (.pkl)
│   ├── data/                    # Dataset used for training
│   └── utils/                   # Feature engineering helpers
│
├── frontend/
│   └── app.py                   # Streamlit dashboard
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🌐 Live Deployment

### 🔗 Backend (FastAPI)

```
https://carbon-smart-charging-scheduler-jnc5.onrender.com
```

### 🔗 Frontend (Streamlit)

```
https://<your-streamlit-app>.streamlit.app
```

---

## 🔌 API Endpoints

### 1️⃣ User Clustering

```http
POST /cluster_user
```

**Input**

```json
{
  "arrival_hour": 18,
  "charging_duration": 3.5,
  "energy_consumed": 40
}
```

**Output**

```json
{
  "user_type": "Flexible User"
}
```

---

### 2️⃣ Carbon Intensity Prediction

```http
POST /predict_carbon
```

**Input**

```json
{
  "timestamp": "2026-01-15T18:30:00"
}
```

**Output**

```json
{
  "predicted_carbon_intensity": 420
}
```

---

## 📊 Machine Learning Highlights

* **StandardScaler** applied before clustering
* No hard‑coded temporal inputs — timestamp only
* Models trained with leakage‑safe preprocessing
* Version‑safe model persistence

---

## 🧪 How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/AnushkaGarade/Carbon_Smart_Charging_Scheduler.git
cd Carbon_Smart_Charging_Scheduler
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Backend

```bash
cd backend
uvicorn main:app --reload
```

### 4️⃣ Run Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 🎯 Future Enhancements

* Real‑time carbon intensity APIs
* Reinforcement learning for charging decisions
* User‑specific cost optimization
* Grid load forecasting integration

---

## 👩‍💻 Author

**Anushka Garade**
BE – Information Technology
Project: *Carbon‑Smart EV Charging Scheduler*

---

## ⭐ Acknowledgements

This project demonstrates the **practical application of machine learning for sustainability**, combining data science, software engineering, and clean‑energy awareness.

If you found this project useful, feel free to ⭐ the repository.
