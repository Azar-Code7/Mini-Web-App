# Mini Web App

A simple web application built with Flask and SQLite.

## Features

* User registration
* User login and logout
* Password hashing
* Session-based authentication
* User dashboard
* User management
* Create, Read, Update and Delete (CRUD)
* Form validation
* Email validation
* SQLite database
* Responsive design

## Technologies

* Python
* Flask
* SQLite
* HTML
* CSS
* Jinja2

## Project Structure

```text
Mini-Web-App/
├── app.py
├── users.db
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── form.html
│   ├── users.html
│   ├── edit.html
│   ├── login.html
│   └── dashboard.html
└── static/
    └── style.css
```

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```powershell
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Database

The application uses SQLite to store user information.

Passwords are stored as secure password hashes rather than plain text.

## Author

Mohammad Eshagh Azar