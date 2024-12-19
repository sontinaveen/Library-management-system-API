import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from config import Config
import time

def get_db_connection():
    """Create a database connection with retry mechanism."""
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            conn = sqlite3.connect(Config.DATABASE_PATH, timeout=10)
            return conn
        except sqlite3.OperationalError as e:
            if attempt < max_attempts - 1:
                # Wait and retry
                time.sleep(0.1)
            else:
                # Re-raise the last exception
                raise

def create_user_table():
    """Create users and tokens tables in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Create tokens table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                token TEXT UNIQUE NOT NULL,
                expires_at DATETIME NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                       (username, hashed_password))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticate a user and return user_id if credentials are valid."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', 
                       (username, hashed_password))
        user = cursor.fetchone()
        return user[0] if user else None
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def generate_token(user_id):
    """Generate a new authentication token for a user."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Generate a secure URL-safe token
        token = secrets.token_urlsafe(32)
        
        # Set token expiration
        expires_at = datetime.now() + timedelta(minutes=Config.TOKEN_EXPIRATION)
        
        # Remove any existing tokens for this user
        cursor.execute('DELETE FROM tokens WHERE user_id = ?', (user_id,))
        
        # Insert new token
        cursor.execute('INSERT INTO tokens (user_id, token, expires_at) VALUES (?, ?, ?)', 
                       (user_id, token, expires_at))
        
        conn.commit()
        return token
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def validate_token(token):
    """Validate an authentication token and return user_id if valid."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if token exists and is not expired
        cursor.execute('SELECT user_id, expires_at FROM tokens WHERE token = ?', (token,))
        result = cursor.fetchone()
        
        if result:
            user_id, expires_at = result
            expires_at = datetime.fromisoformat(expires_at)
            
            # Check if token is still valid
            if expires_at > datetime.now():
                return user_id
        
        return None
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()