# Smart Agriculture Advisory System

The **Smart Agriculture Advisory System** is a full-stack Web Application designed to assist farmers in making informed agricultural decisions. The system provides personalized crop recommendations, weather-based advisories, fertilizer calculator, pest & disease identification catalog, irrigation scheduling, daily mandi market prices (APMC), news feeds, and government schemes catalog. It also provides a comprehensive administration panel for managing all system entities.

Developed using Python Flask (Backend), SQLAlchemy (ORM), and Bootstrap 5 (Frontend), this project is structured for easy setup, testing, and submission.

---

## Features

- **Personalized Crop Recommendations**: Recommends crops based on soil, location, and seasonal parameters.
- **Weather Advisory**: Regional weather forecasts coupled with specific agronomic guidance.
- **Fertilizer Advisor**: Calculates crop-specific fertilizer doses and details safety procedures.
- **Pest & Disease Diagnosis**: Comprehensive database containing symptoms, causes, prevention, and treatment recommendations.
- **Irrigation Advisory**: Guidelines on water requirement metrics and conservation schedules.
- **APMC Mandi Market Prices**: Search, filter by crop or market, and sort by price per quintal.
- **Agricultural News & Govt Schemes**: Centralized directories with apply links and notifications.
- **Farmer Feedback**: Submissions panel with status logs.
- **Admin Control Panel**: Full CRUD operations for Users, Crops, Fertilizers, Weather Tips, Pests, Diseases, Irrigation, Mandi Prices, News, and Schemes.
- **System Reports**: Interactive data charts (using Chart.js), CSV spreadsheet exports, and print styling support.
- **Bilingual Interface**: Quick interface language toggling (English & Kannada).
- **Dark Mode**: Persisted theme switcher.
- **Form Validations**: Advanced client-side and server-side validation.

---

## Folder Structure

```
Smart_Agriculture_Advisory_system/
│
├── app/
│   ├── __init__.py          # Flask app initialization, database & extension setup
│   ├── config.py            # Configuration settings (secret keys, DB connection)
│   ├── models.py            # SQLAlchemy Database models (15 tables)
│   ├── static/              # Public assets
│   │   ├── css/
│   │   │   └── style.css    # Custom styles (agriculture theme, dark mode, prints)
│   │   ├── js/
│   │   │   ├── main.js      # Bilingual translation dictionary, dark mode, form validation
│   │   │   ├── farmer.js    # Farmer module JS (table searches, filters, sorts)
│   │   │   └── admin.js     # Admin module JS (Chart.js stats, delete confirmations)
│   │   └── uploads/         # Uploaded images (profile pictures)
│   ├── templates/           # HTML templates using Jinja2 inheritance
│   │   ├── base.html        # Public navbar & footer
│   │   ├── farmer_base.html # Farmer dashboard sidebar layout
│   │   ├── admin_base.html  # Admin panel sidebar layout
│   │   ├── public/          # Landing pages and login/registration forms
│   │   ├── farmer/          # Farmer advisory dashboards
│   │   └── admin/           # Admin CRUD dashboards and reports
│   └── routes/              # Blueprint routes
│       ├── public.py        # Authentication & Public pages
│       ├── farmer.py        # Farmer modules
│       └── admin.py         # Admin modules & CSV exports
│
├── requirements.txt         # Project dependencies
├── schema.sql               # Raw MySQL Database Schema
├── sample_data.sql          # Seed SQL queries for MySQL testing
├── run.py                   # Server starter script
└── README.md                # Project documentation
```

---

## Installation & Setup Guide

### 1. Prerequisites
- **Python 3.8+** must be installed.
- **MySQL Server** (Optional, falls back to SQLite out-of-the-box).

### 2. Extract & Install Dependencies
Open your terminal (PowerShell / Command Prompt) in the project root directory and run:

```bash
# Optional: Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt
```

### 3. Database Configuration
By default, the application will automatically create and seed a local SQLite database file `app/smart_agri.db` so the system can run instantly with zero configuration.

To configure and connect the system to your local **MySQL Server**, set the following environment variables or edit `app/config.py`:
- Set `DB_TYPE` to `'mysql'`
- Set `DB_USER` (e.g. `'root'`)
- Set `DB_PASSWORD` (e.g. `'password'`)
- Set `DB_HOST` (e.g. `'localhost'`)
- Set `DB_NAME` (e.g. `'smart_agri'`)

Or import and run `schema.sql` and `sample_data.sql` directly on your MySQL instance:
```sql
mysql -u root -p < schema.sql
mysql -u root -p < sample_data.sql
```

### 4. Running the Web Application
Start the Flask local development server by executing:

```bash
python run.py
```

The application will start running on: **`http://127.0.0.1:5000/`**

---

## Default Login Credentials for Testing

To login and inspect the dashboards without registering, use the following pre-seeded credentials:

### Farmer Account
- **Username**: `farmer`
- **Password**: `farmer123`

### Administrator Account
- **Username**: `admin`
- **Password**: `admin123`
