# Mechanic Shop API

A comprehensive RESTful API built with Flask for managing mechanic shop operations, featuring advanced capabilities including token authentication, rate limiting, caching, customer management, mechanic records, service ticket tracking, inventory management, and complex many-to-many relationships.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)

## ✨ Features

### Core Features
- **Customer Management**: Full CRUD operations for customer records with pagination support
- **Mechanic Management**: Full CRUD operations for mechanic profiles with salary tracking
- **Service Tickets**: Create and manage service tickets with VIN tracking
- **Inventory Management**: Complete CRUD operations for auto parts and inventory items
- **Many-to-Many Relationships**: 
  - Assign multiple mechanics to service tickets
  - Link multiple inventory parts to service tickets
- **Data Validation**: Marshmallow schemas for comprehensive request/response validation
- **Application Factory Pattern**: Modular and scalable Flask application architecture
- **Blueprint Organization**: Cleanly separated API routes by resource type

### Advanced Features
- **🔐 Token Authentication**: JWT-based authentication using `encode_token()` and `@token_required` decorator
- **🔒 Login System**: Secure customer login with email/password validation using dedicated `login_schema`
- **⚡ Rate Limiting**: Flask-Limiter integration to prevent API abuse (5 requests per day for customer creation, 5 per month for updates)
- **💾 Caching**: Flask-Caching with 60-second timeout for frequently accessed endpoints
- **📄 Pagination**: Query parameter-based pagination on GET /customers endpoint (default: 10 per page)
- **🎯 Advanced Queries**: 
  - `/mechanics/by-ticket-count` - Mechanics ordered by number of tickets worked (DESC)
  - Dynamic mechanic assignment/removal from tickets
  - Inventory part linking to service tickets
- **🎫 My Tickets Route**: Token-protected `/my-tickets` endpoint for authenticated customers to view their service tickets

## 🛠️ Tech Stack

- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0.46 with Flask-SQLAlchemy 3.1.1
- **Serialization**: Marshmallow 4.2.1 with Flask-Marshmallow 1.3.0 and marshmallow-sqlalchemy 1.4.2
- **Database**: MySQL (mysql-connector-python 9.5.0)
- **Rate Limiting**: Flask-Limiter 4.1.1
- **Caching**: Flask-Caching 2.3.1
- **Authentication**: PyJWT 2.11.0
- **Server**: Werkzeug 3.1.5

## 📁 Project Structure

```
mechanic-shop-api/
├── app/
│   ├── Blueprints/
│   │   ├── Customer/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py       # Customer endpoints + login + my-tickets
│   │   │   └── schemas.py      # customer_schema, customers_schema, login_schema
│   │   ├── Mechanics/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py       # Mechanic endpoints + by-ticket-count query
│   │   │   └── schemas.py
│   │   ├── Service_tickets/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py       # Service ticket endpoints + mechanic/part assignment
│   │   │   └── schemas.py
│   │   └── Inventory/
│   │       ├── __init__.py
│   │       ├── routes.py       # Inventory CRUD operations
│   │       └── schemas.py
│   ├── __pycache__/
│   ├── static/
│   │   └── swagger.yaml                    # Swagger/OpenAPI documentation
│   ├── utils/
│   │   └── util.py             # encode_token, token_required decorator
│   ├── __init__.py             # Application factory + extensions initialization
│   ├── models.py               # Database models with many-to-many relationships
│   └── extensions.py           # Extensions (db, ma, limiter, cache)
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
└── requirements.txt            # Python dependencies
├── tests/
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_inventory.py
│   ├── test_mechanics.py
│   └── test_service_tickets.py
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/pperez90-lab/advanced-mechanic-shop-api.git
cd advanced-mechanic-shop-api
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**
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
    SECRET_KEY = 'your-secret-key-here'  # Required for JWT token encoding

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

**Important**: Replace `username`, `password`, and `database_name` with your MySQL credentials. Set a strong `SECRET_KEY` for production use.

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

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/customers/login` | Customer login - returns JWT token | No |

**Request Body** (login_schema):
```json
{
  "email": "customer@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "You have successfully been logged in.",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Customers

| Method | Endpoint | Description | Rate Limit | Cache | Auth |
|--------|----------|-------------|------------|-------|------|
| POST | `/customers/` | Create a new customer | 5/day | No | No |
| GET | `/customers/` | Get all customers (paginated) | No | 60s | No |
| GET | `/customers/<id>` | Get a specific customer | No | No | No |
| PUT | `/customers/` | Update authenticated customer | 5/month | No | Yes |
| DELETE | `/customers/` | Delete authenticated customer | 5/day | No | Yes |

**Pagination Parameters** (GET `/customers/`):
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10)

Example: `GET /customers/?page=2&per_page=20`

### Mechanics

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mechanics/` | Create a new mechanic |
| GET | `/mechanics/` | Get all mechanics |
| GET | `/mechanics/<id>` | Get a specific mechanic |
| PUT | `/mechanics/<id>` | Update a mechanic |
| DELETE | `/mechanics/<id>` | Delete a mechanic |
| **GET** | **`/mechanics/by-ticket-count`** | **Get mechanics ordered by tickets worked (advanced query)** |

### Service Tickets

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/service-tickets/` | Create a new service ticket | No |
| GET | `/service-tickets/` | Get all service tickets | No |
| **GET** | **`/service-tickets/my-tickets`** | **Get tickets for authenticated customer** | **Yes (Token)** |
| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket | No |
| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket | No |
| PUT | `/service-tickets/<ticket_id>/add-part/<inventory_id>` | Add inventory part to ticket | No |

### Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/inventory/` | Create a new inventory item |
| GET | `/inventory/` | Get all inventory items |
| GET | `/inventory/<id>` | Get a specific inventory item |
| PUT | `/inventory/<id>` | Update an inventory item |
| DELETE | `/inventory/<id>` | Delete an inventory item |

## 🔐 Authentication

### How to Use Token Authentication

1. **Login to get a token**:
   ```bash
   curl -X POST http://127.0.0.1:5000/customers/login \
     -H "Content-Type: application/json" \
     -d '{"email": "customer@example.com", "password": "password123"}'
   ```

2. **Use the token in protected endpoints**:
   ```bash
   curl -X GET http://127.0.0.1:5000/service-tickets/my-tickets \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

### Protected Endpoints
- `GET /service-tickets/my-tickets` - View your service tickets
- `PUT /customers/` - Update your profile
- `DELETE /customers/` - Delete your account

## 💡 Usage Examples

### Create a Customer

```bash
curl -X POST http://127.0.0.1:5000/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "password": "securepass123"
  }'
```

### Login and Get Token

```bash
curl -X POST http://127.0.0.1:5000/customers/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
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

### Get My Tickets (Authenticated)

```bash
curl -X GET http://127.0.0.1:5000/service-tickets/my-tickets \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Assign a Mechanic to a Ticket

```bash
curl -X PUT http://127.0.0.1:5000/service-tickets/1/assign-mechanic/1
```

### Add Inventory Part to Ticket

```bash
curl -X PUT http://127.0.0.1:5000/service-tickets/1/add-part/5
```

### Get Mechanics by Ticket Count (Advanced Query)

```bash
curl http://127.0.0.1:5000/mechanics/by-ticket-count
```

### Get Paginated Customers

```bash
curl "http://127.0.0.1:5000/customers/?page=1&per_page=10"
```


## 🧪 Testing

This project includes comprehensive unit tests for all major components.

### Running Tests

To run the test suite:

```bash
python -m pytest tests/
```

Run tests with coverage:

```bash
python -m pytest tests/ --cov=app --cov-report=html
```

### Test Files

- `test_customers.py` - Customer CRUD operations and authentication tests
- `test_mechanics.py` - Mechanic management tests
- `test_inventory.py` - Inventory CRUD tests
- `test_service_tickets.py` - Service ticket and many-to-many relationship tests

### API Documentation

Swagger/OpenAPI documentation is available at:
- File: `app/static/swagger.yaml`
- Access it by serving the static folder or importing into Swagger UI
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

Built with ❤️ using Flask, SQLAlchemy, and advanced API development practices
