
# 🌆 Cypress Reporting System

A Flask-based web application that enables Toronto residents to report and track non-emergency street-level issues — including potholes, graffiti, and broken streetlights.

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue.svg)

---

## 🚀 Features

- 🔐 User Authentication (Sign Up / Login)
- 🗺️ Interactive Map for Pinpointing Issues
- 📝 Categorization via Dropdown + Free-Text Description
- 🔄 Smart Report Deduplication by Location
- 🗃️ Persistent Data Storage with SQLite
- 🛠️ Admin Panel for Reviewing Reports

---

## 🗂️ Project Structure

```bash
Cps406Project/
│
├── app.py             # Main Flask application
├── database.py        # DB schema and queries
├── utils.py           # Helper functions
├── cypress.db         # SQLite database
│
├── templates/         # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── admin.html
│
├── static/            # Static files (CSS, JS)
│   ├── style.css
│   └── script.js
│
├── README.md
└── README.txt         # Delivery Package (for course submission)
```

---

## 🛠️ How to Run

1. Install dependencies:
   ```bash
   pip install Flask
   ```

2. Launch the app:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 👨‍💻 Team Members

- **Anvit Bindra** — `501275606`
- **Isaac Efrat** — `501248396`
- **Vishal Bharti** — `501240769`
- **Rhett Williams** — `501265397`
- **Raiden Oreta** — `501112245`
- **Max Quattrociocchi** — `501233904`

---

## 📄 License

This project is for academic purposes only and is not licensed for commercial use.
