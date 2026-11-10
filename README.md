# EventNest – Event Booking Platform

A Django-based event discovery and ticket booking platform that allows users to explore events, view event details, book tickets, and manage their bookings.

## 🚀 Features

- User Registration and Login
- Browse Upcoming Events
- Search Events by Title and Location
- Category-based Event Filtering
- Individual Event Details
- Online Ticket Booking
- Unique Booking ID Generation
- Booking Confirmation and Printable E-Ticket
- My Bookings Dashboard
- Booking Cancellation
- Automatic Ticket Availability Updates
- Django Admin Panel for Event Management
- Responsive User Interface

## 🛠️ Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Version Control:** Git and GitHub
- **Development Tool:** VS Code

## 📂 Project Structure

```text
EventNest/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── events/
│   ├── migrations/
│   ├── templates/
│   │   └── events/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Teja-Adimoolam/EventNest.git
```

### 2. Navigate to the project folder

```bash
cd EventNest
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment (Windows)

```powershell
venv\Scripts\activate
```

### 5. Install Django

```bash
pip install Django
```

### 6. Set the Django Secret Key

Generate a new secret key and set it in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "your-secret-key"
```

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open your browser:

http://127.0.0.1:8000/

## 🔮 Future Improvements

- Payment Gateway Integration
- Email Booking Confirmation
- User Profile Management
- Event Reviews and Ratings
- Advanced Event Filters

## 👨‍💻 Developer

**Teja Adimoolam**

GitHub: https://github.com/Teja-Adimoolam

---

⭐ If you find this project interesting, feel free to explore the repository!
