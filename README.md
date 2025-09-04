# 🚀 FastAPI Backend Template

A modern, production-ready FastAPI backend template with clean architecture, async database operations, and comprehensive features for building scalable web applications.

## ✨ Features

- **🚀 FastAPI Framework** - High-performance, modern web framework for building APIs
- **🐢 Tortoise ORM** - Async database ORM with automatic migrations
- **🔐 JWT Authentication** - Secure user authentication and authorization
- **📊 Database** - database with automatic migrations
- **🏗️ Clean Architecture** - Well-structured, maintainable codebase
- **📝 Pydantic Validation** - Data validation and serialization
- **🔒 Security Middleware** - Rate limiting, CORS, and authentication
- **📋 Comprehensive Testing** - Unit tests with pytest
- **📚 Auto-generated API Docs** - Swagger UI and ReDoc
- **📊 Logging & Monitoring** - Structured logging and health checks

## 🏗️ Project Structure

```
MyApp/
├── app/
│   ├── api/                    # API endpoints and routers
│   │   └── v1/                # API version 1
│   │       └── users.py       # User management endpoints
│   ├── core/                  # Core configuration and utilities
│   │   ├── config.py          # Application settings
│   │   ├── db.py              # Database configuration
│   │   ├── security.py        # JWT and security utilities
│   │   └── logging.py         # Logging configuration
│   ├── middleware/            # Custom middleware
│   │   ├── auth.py            # Authentication middleware
│   │   ├── logging.py         # Request logging
│   │   └── rate_limit.py      # Rate limiting
│   ├── models/                # Database models (Tortoise ORM)
│   │   └── user.py            # User model
│   ├── repositories/          # Data access layer
│   │   └── user_repo.py       # User repository
│   ├── schemas/               # Pydantic schemas
│   │   └── user.py            # User data validation
│   ├── services/              # Business logic layer
│   │   └── user_service.py    # User business logic
│   ├── utils/                 # Utility functions
│   │   ├── cache.py           # Caching utilities
│   │   └── email.py           # Email utilities
│   └── main.py                # FastAPI application entry point
├── tests/                     # Test suite
├── migrations/                # Database migrations (Aerich)
├── requirements.txt            # Python dependencies
├── aerich.ini                 # Migration configuration
├── run.py                     # Application runner
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saydullayev/fastapi-backend-template.git
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize database**
   ```bash
   aerich init --tortoise-orm app.core.config.settings
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register a new user**
   ```bash
   POST /api/v1/users/register
   {
     "username": "john_doe",
     "email": "john@example.com",w
     "password": "secure_password"
   }
   ```

2. **Login to get access token**
   ```bash
   POST /api/v1/users/login
   {
     "username": "john_doe",
     "password": "secure_password"
   }
   ```

3. **Use the token in subsequent requests**
   ```bash
   Authorization: Bearer <your_access_token>
   ```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

## 🚀 Production Deployment

### Environment Variables

Create a `.env` file with production settings:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key-here
DEBUG=false
LOG_LEVEL=WARNING
```

### Database

For production, consider using PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install asyncpg

# Update database URL in .env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Running with Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🔧 Configuration

Key configuration options in `app/core/config.py`:

- `database_url`: Database connection string
- `secret_key`: JWT secret key
- `access_token_expire_minutes`: Token expiration time
- `debug`: Debug mode flag
- `log_level`: Logging level

## 📝 API Endpoints

### Users
- `POST /api/v1/users/register` - User registration
- `POST /api/v1/users/login` - User authentication
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/) - Async ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Aerich](https://github.com/tortoise/aerich) - Database migrations

## 📞 Support

If you have any questions or need help:

- Create an [Issue](https://github.com/Saydullayev/fastapi-backend-template/issues)
- Check the [Documentation](https://github.com/Saydullayev/fastapi-backend-template/wiki)
- Join our [Discussions](https://github.com/Saydullayev/fastapi-backend-template/discussions)

---

⭐ **Star this repository if you find it helpful!**
