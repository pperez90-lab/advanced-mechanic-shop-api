# Mechanic Shop API

A comprehensive RESTful API built with Flask for managing mechanic shop operations. This system features token-based authentication, rate limiting, and caching to ensure a secure and high-performance experience.

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
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [Contributing](#contributing)

## ✨ Features

### Core Operations
- **Customer Management**: Full CRUD with pagination and secure login.
- **Mechanic Management**: Manage profiles, salary tracking, and performance.
- **Service Tickets**: Create and track tickets with VIN association.
- **Inventory Tracking**: Manage parts and inventory levels.

### Advanced Capabilities
- **🔐 Security**: JWT token authentication with `@token_required` decorators.
- **⚡ Performance**: Flask-Caching (60s) for frequently accessed data.
- **🛡️ Protection**: Flask-Limiter to prevent API abuse.
- **🔗 Relationships**: Complex many-to-many links between tickets, mechanics, and parts.

## 🛠️ Tech Stack

- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0.46
- **Database**: MySQL 9.5.0
- **Validation**: Marshmallow 4.2.1
- **CI/CD**: GitHub Actions
- **Auth**: PyJWT 2.11.0

## 🚀 Installation

1. **Clone & Navigate**:
   ```bash
   git clone https://github.com/pperez90-lab/advanced-mechanic-shop-api.git
   cd advanced-mechanic-shop-api
   ```

2. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   venv\Scripts\activate     # Windows
   ```

3. **Install Deps**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create `config.py` in the root:
```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:pass@localhost/mechanic_shop'
    SECRET_KEY = 'your-secure-key'
```

## 🗄️ Database Setup

```sql
CREATE DATABASE mechanic_shop;
```
Initialize tables via Flask shell:
```python
from app.extensions import db
db.create_all()
```

## 🧪 Testing

Run the test suite with coverage:
```bash
python -m pytest tests/ --cov=app
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for Continuous Integration and Deployment.
- **CI**: Automated testing on pushes to `main` and `master`.
- **CD**: Automatic deployment to **Render** upon successful test completion.

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a PR for any improvements.

---
**Author**: Peter Perez | Built with ❤️ using Flask and SQLAlchemy.
