# Library Management System:

# Project Overview:

A robust Flask-based Library Management System with comprehensive features for managing library resources efficiently.

# Features:

- Full CRUD Operations for Books
- Advanced Search Functionality
Token-Based Authentication
Pagination Support
SQLite Database Integration

# Prerequisites:

- Python 3.8+
- pip
- Virtual Environment (recommended)

# Installation:

1)Create and activate a virtual environment

- python -m venv venv
- venv\Scripts\activate

2)Install dependencies

- pip install -r requirements.txt

3) Initialize the database
- python -c "from models import Book, User; Book.create_table(); User.create_table()"


# Running the Application:

- python app.py

# Authentication:

- - `POST /register`: Create a new user account
- - Request Body: `{"username": "string", "password": "string"}`

- - `POST /login`: Authenticate and receive token
  - Request Body: `{"username": "string", "password": "string"}`
  - Response: `{"token": "authentication_token"}`

# Book Management:

- `POST /books`: Add a new book (Authenticated)
  - Request Body: 
    ```json
    {
      "title": "Book Title",
      "author": "Author Name",
      "isbn": "1234567890",
      "publication_year": 2023,
      "quantity": 10
    }
    ```
- `GET /books`: List books with pagination
  - Query Params: `page=1`
- `GET /books/search`: Search books
  - Query Params: `query=searchterm&page=1`
- `GET /books/<book_id>`: Get specific book details
- `PUT /books/<book_id>`: Update book information
- `DELETE /books/<book_id>`: Remove a book

# PostMan:
 - To test and interact with APIs

# Authentication Flow:

1. Register a new user
2. Login to receive an authentication token
3. Include token in `Authorization` header for subsequent requests

# Configuration:

Modify `config.py` to adjust:
- Secret Key
- Pagination Settings
- Token Expiration Time