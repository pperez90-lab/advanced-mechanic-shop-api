# Mechanic Shop API

A RESTful API built with Flask for managing mechanic shop operations, including customer management, mechanic records, and service ticket tracking with many-to-many relationships.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)

## ✨ Features

- **Customer Management**: Full CRUD operations for customer records
- **Mechanic Management**: Full CRUD operations for mechanic profiles with salary tracking
- **Service Tickets**: Create and manage service tickets with VIN tracking
- **Many-to-Many Relationships**: Assign multiple mechanics to service tickets
- **Data Validation**: Marshmallow schemas for request/response validation
- **Application Factory Pattern**: Modular and scalable Flask application architecture
- **Blueprint Organization**: Cleanly separated API routes by resource type

## 🛠️ Tech Stack

- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0.46 with Flask-SQLAlchemy 3.1.1
- **Serialization**: Marshmallow 4.2.1 with Flask-Marshmallow 1.3.0 and marshmallow-sqlalchemy 1.4.2
- **Database**: MySQL (mysql-connector-python 9.5.0)
- **Server**: Werkzeug 3.1.5

## 📁 Project Structure

```
mechanic-shop-api/
├── app/
│   ├── Blueprints/
│   │   ├── Customer/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── Mechanics/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   └── Service_tickets/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/pperez90-lab/mechanic-shop-api.git
cd mechanic-shop-api
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `config.py` file in the root directory with your database configuration:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

**Important**: Replace `username`, `password`, and `database_name` with your MySQL credentials.

## 🗄️ Database Setup

1. **Create a MySQL database**

```sql
CREATE DATABASE mechanic_shop;
```

2. **Initialize the database tables**

Run the Flask shell to create tables:

```bash
flask shell
```

Then execute:

```python
from app.extensions import db
db.create_all()
exit()
```

## ▶️ Running the Application

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## 📚 API Endpoints

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/customers/` | Create a new customer |
| GET | `/customers/` | Get all customers |
| GET | `/customers/<id>` | Get a specific customer |
| PUT | `/customers/<id>` | Update a customer |
| DELETE | `/customers/<id>` | Delete a customer |

### Mechanics

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mechanics/` | Create a new mechanic |
| GET | `/mechanics/` | Get all mechanics |
| GET | `/mechanics/<id>` | Get a specific mechanic |
| PUT | `/mechanics/<id>` | Update a mechanic |
| DELETE | `/mechanics/<id>` | Delete a mechanic |

### Service Tickets

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/service-tickets/` | Create a new service ticket |
| GET | `/service-tickets/` | Get all service tickets |
| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket |
| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket |

## 💡 Usage Examples

### Create a Customer

```bash
curl -X POST http://127.0.0.1:5000/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-0123"
  }'
```

### Create a Service Ticket

```bash
curl -X POST http://127.0.0.1:5000/service-tickets/ \
  -H "Content-Type: application/json" \
  -d '{
    "VIN": "1HGBH41JXMN109186",
    "service_date": "2026-02-10",
    "service_desc": "Oil change and tire rotation",
    "customer_id": 1
  }'
```

### Assign a Mechanic to a Ticket

```bash
curl -X PUT http://127.0.0.1:5000/service-tickets/1/assign-mechanic/1
```

### Get All Customers

```bash
curl http://127.0.0.1:5000/customers/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available for educational purposes.

## 👤 Author

**Peter Perez**
- GitHub: [@pperez90-lab](https://github.com/pperez90-lab)

---

Built with ❤️ using Flask and SQLAlchemy
