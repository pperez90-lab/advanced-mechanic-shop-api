# Mechanic Shop API

A comprehensive RESTful API built with Flask for managing mechanic shop operations. This system features token-based authentication, rate limiting, and caching to ensure a secure and high-performance experience.

📋 Table of Contents
--------------------

*   • [Features](#features)
*   • [Tech Stack](#tech-stack)
*   • [Project Structure](#project-structure)
*   • [Installation](#installation)
*   • [Configuration](#configuration)
*   • [Database Setup](#database-setup)
*   • [Running the Application](#running-the-application)
*   • [API Endpoints](#api-endpoints)
*   • [Authentication](#authentication)
*   • [CI/CD Pipeline](#cicd-pipeline)
*   • [Usage Examples](#usage-examples)
*   • [Testing](#testing)
*   • [Contributing](#contributing)

✨ Features
----------

### Core Features
*   • **Customer Management**: Full CRUD operations for customer records with pagination support
*   • **Mechanic Management**: Full CRUD operations for mechanic profiles with salary tracking
*   • **Service Tickets**: Create and manage service tickets with VIN tracking
*   • **Inventory Management**: Complete CRUD operations for auto parts and inventory items
*   • **Many-to-Many Relationships**:
    *   ◦ Assign multiple mechanics to service tickets
    *   ◦ Link multiple inventory parts to service tickets

### Advanced Capabilities
*   • **🔐 Security**: JWT token authentication with `@token_required` decorators.
*   • **⚡ Performance**: Flask-Caching (60s) for frequently accessed data.
*   • **🛡️ Protection**: Flask-Limiter to prevent API abuse.
*   • **🎯 Advanced Queries**: `/mechanics/by-ticket-count` and dynamic resource assignment.

🛠️ Tech Stack
--------------

- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0.46 with Flask-SQLAlchemy 3.1.1
- **Database**: MySQL 9.5.0 (mysql-connector-python)
- **CI/CD**: GitHub Actions
- **Auth**: PyJWT 2.11.0
- **Rate Limiting**: Flask-Limiter 4.1.1
- **Caching**: Flask-Caching 2.3.1

📁 Project Structure
--------------------

```
mechanic-shop-api/
├── app/
│   ├── Blueprints/
│   │   ├── Customer/
│   │   ├── Mechanics/
│   │   ├── Service_tickets/
│   │   └── Inventory/
│   ├── utils/
│   │   └── util.py # Auth decorators
│   ├── static/
│   │   └── swagger.yaml
│   ├── models.py # DB Models
│   └── extensions.py # Extensions init
├── app.py # Entry point
├── config.py # Config settings
└── tests/ # Unit tests
```

🚀 Installation
---------------

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

⚙️ Configuration
----------------

Create `config.py` in the root:
```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:pass@localhost/mechanic_shop'
    SECRET_KEY = 'your-secure-key'
```

🗄️ Database Setup
------------------

```sql
CREATE DATABASE mechanic_shop;
```
Initialize tables via Flask shell:
```python
from app.extensions import db
db.create_all()
```

▶️ Running the Application
--------------------------

```bash
python app.py
```
The API will be available at `http://127.0.0.1:5000`

📚 API Endpoints
----------------

Detailed endpoint documentation and tables are available in the repository. Major resource groups include:
- **/customers**: Login, CRUD, and pagination.
- **/mechanics**: CRUD and ticket count queries.
- **/service-tickets**: Ticket management and resource assignment.
- **/inventory**: Parts and stock management.

🔐 Authentication
-----------------

The API uses Bearer Token authentication.
1. POST to `/customers/login` with credentials.
2. Receive JWT token.
3. Include `Authorization: Bearer <token>` in headers for protected routes.

🔄 CI/CD Pipeline
-----------------

The project uses GitHub Actions for CI/CD.
- **CI**: Automated tests run on every push to `main`.
- **CD**: Successful builds are automatically deployed to **Render**.

💡 Usage Examples
-----------------

```bash
# Login Example
curl -X POST http://127.0.0.1:5000/customers/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'
```

🧪 Testing
----------

Run tests with coverage:
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

🤝 Contributing
---------------

Contributions are welcome! Please fork the repo and submit a PR.

---
**Author**: Peter Perez | Built with ❤️ using Flask and SQLAlchemy.
