# Heritage Brew — Artisanal Craft Soda E-Commerce

A clean, sophisticated, full-stack e-commerce web platform for **Heritage Brew Co.**, a small-batch artisanal craft soft drink micro-brewery.

Built using **HTML5, CSS3, JavaScript, Python, Django, and MySQL**.

---

## 🌟 Features

- **Artisanal Aesthetics**: Vintage-modern craft branding with warm bourbon amber tones, dark glassmorphism, and responsive typography (Playfair Display, Cinzel, Plus Jakarta Sans).
- **Curated Micro-Batch Catalog**: Complete product showcase with tasting notes, botanical ingredients, sommelier pairings, and volume specifications.
- **Dynamic Crate Sizing**: Instant client-side pack selector for Single Bottle, 4-Pack Box, and 12-Pack Collector's Case with real-time price updates.
- **Session-Based Shopping Crate**: Interactive crate drawer and dedicated cart page with quantity increment/decrement and a Complimentary Shipping progress indicator ($40 threshold).
- **Interactive Reviews**: Verified sommelier tasting reviews with star ratings and a live submission form.
- **Secure Dispatch Checkout**: Clean destination form, payment method selector (Cash on Delivery, Simulated Card, UPI), unique order generation (`HB-XXXXXX`), and printable receipts.
- **Dual Database Support**: Seamless integration with local **MySQL80** via PyMySQL, with automatic SQLite fallback if credentials are not yet specified in `.env`.
- **Django Admin Portal**: Full management of products, categories, orders, order items, reviews, contact messages, and newsletter subscribers.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14+, Django 6.1
- **Database**: MySQL 8.0 (with fallback to SQLite3)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), JavaScript (ES6+ / AJAX)
- **Icons & Fonts**: Font Awesome 6.5, Google Fonts (Cinzel, Playfair Display, Plus Jakarta Sans)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- MySQL 8.0 (optional, fallback SQLite works automatically)

### 2. Setup Environment & Dependencies
```bash
pip install django pymysql cryptography python-dotenv pillow
```

### 3. Configure Database
Copy `.env.example` to `.env` and enter your MySQL credentials if using MySQL:
```env
USE_MYSQL=True
DB_NAME=heritage_drinks_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 4. Run Migrations & Seed Data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Administrative Access
- **Admin Portal**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 📂 Project Structure

```
├── heritage_brew/          # Django Project Configuration
│   ├── __init__.py         # PyMySQL driver configuration
│   ├── settings.py         # App settings & dynamic DB selection
│   ├── urls.py             # Root URL routing & static/media handlers
│   └── wsgi.py
├── store/                  # Store Application
│   ├── static/store/       # CSS, JS, and photorealistic craft soda images
│   ├── templates/store/    # Base layout and page templates
│   ├── management/         # Custom seed_data command
│   ├── models.py           # Relational schema (Product, Order, Review, etc.)
│   ├── views.py            # Business logic & purchase flows
│   ├── cart.py             # Session crate management
│   ├── forms.py            # Checkout, Review, and Contact forms
│   └── urls.py
├── media/products/         # Product image uploads
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── manage.py
└── README.md
```

---

## 📜 License
Handcrafted for Heritage Brew Co. All rights reserved.
