import sqlite3
from datetime import datetime, timedelta
import secrets
import hashlib
import os
from config import Config

class Book:
    def __init__(self, title, author, isbn, publication_year, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.quantity = quantity

    @staticmethod
    def create_table():
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                publication_year INTEGER,
                quantity INTEGER DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO books (title, author, isbn, publication_year, quantity)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.title, self.author, self.isbn, self.publication_year, self.quantity))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all(page=1, per_page=Config.ITEMS_PER_PAGE):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        offset = (page - 1) * per_page
        cursor.execute('''
            SELECT * FROM books LIMIT ? OFFSET ?
        ''', (per_page, offset))
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def search(query, page=1, per_page=Config.ITEMS_PER_PAGE):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        offset = (page - 1) * per_page
        cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? 
            LIMIT ? OFFSET ?
        ''', (f'%{query}%', f'%{query}%', per_page, offset))
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def get_by_id(book_id):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        conn.close()
        return book

    def update(self, book_id):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE books 
            SET title=?, author=?, isbn=?, publication_year=?, quantity=? 
            WHERE id=?
        ''', (self.title, self.author, self.isbn, self.publication_year, self.quantity, book_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(book_id):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()