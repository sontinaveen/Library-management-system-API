from flask import Flask, request, jsonify, current_app
from models import Book
import auth
from config import DevelopmentConfig
import functools

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize database tables
Book.create_table()
auth.create_user_table()

def token_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        user_id = auth.validate_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        return f(*args, **kwargs)
    return wrapper

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = auth.register_user(data['username'], data['password'])
    
    if user_id:
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    else:
        return jsonify({"error": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = auth.authenticate_user(data['username'], data['password'])
    
    if user_id:
        token = auth.generate_token(user_id)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/books/add', methods=['POST'])
@token_required
def create_book():
    data = request.json
    book = Book(
        title=data['title'], 
        author=data['author'], 
        isbn=data['isbn'], 
        publication_year=data['publication_year'], 
        quantity=data.get('quantity', 1)
    )
    book_id = book.save()
    
    if book_id:
        return jsonify({"message": "Book added successfully", "book_id": book_id}), 201
    else:
        return jsonify({"error": "Book with this ISBN already exists"}), 400

@app.route('/books/list', methods=['GET'])
@token_required
def list_books():
    page = int(request.args.get('page', 1))
    books = Book.get_all(page)
    return jsonify(books), 200

@app.route('/books/search', methods=['GET'])
@token_required
def search_books():
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))
    books = Book.search(query, page)
    return jsonify(books), 200

@app.route('/books/<int:book_id>', methods=['GET'])
@token_required
def get_book(book_id):
    book = Book.get_by_id(book_id)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>/update', methods=['PUT'])
@token_required
def update_book(book_id):
    data = request.json
    book = Book(
        title=data['title'], 
        author=data['author'], 
        isbn=data['isbn'], 
        publication_year=data['publication_year'], 
        quantity=data.get('quantity', 1)
    )
    book.update(book_id)
    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/books/<int:book_id>/delete', methods=['DELETE'])
@token_required
def delete_book(book_id):
    Book.delete(book_id)
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)