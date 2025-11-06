"""
SIMPLE DATABASE MODULE
======================
Easy-to-understand database operations

This handles all interactions with the SQLite database.
Think of it as a librarian who manages all the books!
"""

import sqlite3
import os


class SimpleDatabase:
    """
    A simple database class for managing library data
    
    What it does:
    - Stores books, users, and borrowing records
    - Provides easy functions to add/get/update data
    - Uses SQLite (a simple file-based database)
    """
    
    def __init__(self, db_name='simple_library.db'):
        """
        Initialize the database
        
        Args:
            db_name: Name of the database file
        """
        self.db_name = db_name
        self.create_tables()
    
    
    def get_connection(self):
        """
        Create a connection to the database
        
        Think of this like opening the library door!
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This lets us use column names
        return conn
    
    
    def create_tables(self):
        """
        Create database tables if they don't exist
        
        Tables:
        1. books - Stores all book information
        2. users - Stores user accounts
        3. borrowing - Tracks who borrowed which book
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                year INTEGER,
                description TEXT,
                available_copies INTEGER DEFAULT 1,
                total_copies INTEGER DEFAULT 1
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Borrowing table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowing (
                borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TEXT DEFAULT CURRENT_TIMESTAMP,
                return_date TEXT,
                status TEXT DEFAULT 'borrowed',
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        ''')
        
        # Create indexes for faster searching
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON books(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_author ON books(author)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_genre ON books(genre)')
        
        conn.commit()
        conn.close()
    
    
    # ========================================
    # BOOK OPERATIONS
    # ========================================
    
    def add_book(self, title, author, genre, year=None, description=None, copies=1):
        """
        Add a new book to the library
        
        Example:
            db.add_book('Harry Potter', 'J.K. Rowling', 'Fantasy', 1997)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO books (title, author, genre, year, description, available_copies, total_copies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, genre, year, description, copies, copies))
        
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return book_id
    
    
    def get_all_books(self):
        """
        Get all books from the database
        
        Returns:
            List of book dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books ORDER BY title')
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        books = [dict(row) for row in rows]
        
        conn.close()
        return books
    
    
    def get_book_by_id(self, book_id):
        """
        Get a specific book by its ID
        
        Args:
            book_id: The ID of the book to find
        
        Returns:
            Book dictionary or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    
    def search_books(self, search_term):
        """
        Search for books (title, author, or genre)
        
        This uses SQL LIKE for pattern matching
        
        Example:
            books = db.search_books('Harry')
            # Returns all books with 'Harry' in title/author/genre
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Search pattern - % means "anything before/after"
        pattern = f'%{search_term}%'
        
        cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? 
               OR author LIKE ? 
               OR genre LIKE ?
            ORDER BY title
        ''', (pattern, pattern, pattern))
        
        rows = cursor.fetchall()
        books = [dict(row) for row in rows]
        
        conn.close()
        return books
    
    
    # ========================================
    # USER OPERATIONS
    # ========================================
    
    def add_user(self, username, email):
        """
        Add a new user to the system
        
        Example:
            db.add_user('john_doe', 'john@example.com')
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email)
                VALUES (?, ?)
            ''', (username, email))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            # Username or email already exists
            conn.close()
            return None
    
    
    def get_user(self, user_id):
        """
        Get user information
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    
    # ========================================
    # BORROWING OPERATIONS
    # ========================================
    
    def borrow_book(self, user_id, book_id):
        """
        Let a user borrow a book
        
        Steps:
        1. Check if book is available
        2. Create borrowing record
        3. Decrease available copies
        
        Returns:
            True if successful, False if book not available
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if book is available
        cursor.execute('SELECT available_copies FROM books WHERE book_id = ?', (book_id,))
        row = cursor.fetchone()
        
        if not row or row[0] <= 0:
            conn.close()
            return False  # Book not available
        
        # Create borrowing record
        cursor.execute('''
            INSERT INTO borrowing (user_id, book_id, status)
            VALUES (?, ?, 'borrowed')
        ''', (user_id, book_id))
        
        # Decrease available copies
        cursor.execute('''
            UPDATE books 
            SET available_copies = available_copies - 1 
            WHERE book_id = ?
        ''', (book_id,))
        
        conn.commit()
        conn.close()
        return True
    
    
    def return_book(self, borrow_id):
        """
        Return a borrowed book
        
        Steps:
        1. Update borrowing record
        2. Increase available copies
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get the book_id from borrowing record
        cursor.execute('SELECT book_id FROM borrowing WHERE borrow_id = ?', (borrow_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        book_id = row[0]
        
        # Update borrowing record
        cursor.execute('''
            UPDATE borrowing 
            SET return_date = CURRENT_TIMESTAMP, status = 'returned'
            WHERE borrow_id = ?
        ''', (borrow_id,))
        
        # Increase available copies
        cursor.execute('''
            UPDATE books 
            SET available_copies = available_copies + 1 
            WHERE book_id = ?
        ''', (book_id,))
        
        conn.commit()
        conn.close()
        return True
    
    
    def get_user_borrowed_books(self, user_id):
        """
        Get all books borrowed by a user
        
        Returns both current and past borrowings
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, books.title, books.author, books.genre
            FROM borrowing b
            JOIN books ON b.book_id = books.book_id
            WHERE b.user_id = ?
            ORDER BY b.borrow_date DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        borrowings = [dict(row) for row in rows]
        
        conn.close()
        return borrowings
    
    
    # ========================================
    # STATISTICS
    # ========================================
    
    def get_stats(self):
        """
        Get library statistics
        
        Returns a dictionary with useful numbers:
        - Total books
        - Available books
        - Borrowed books
        - Total users
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total books
        cursor.execute('SELECT COUNT(*) FROM books')
        stats['total_books'] = cursor.fetchone()[0]
        
        # Available books
        cursor.execute('SELECT SUM(available_copies) FROM books')
        stats['available_books'] = cursor.fetchone()[0] or 0
        
        # Currently borrowed
        cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'borrowed'")
        stats['borrowed_books'] = cursor.fetchone()[0]
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        stats['total_users'] = cursor.fetchone()[0]
        
        conn.close()
        return stats


# ============================================
# TESTING CODE
# ============================================

if __name__ == '__main__':
    print("Testing Simple Database...")
    print("=" * 50)
    
    # Create a test database
    db = SimpleDatabase('test.db')
    
    # Add a user
    print("\n1. Adding a user...")
    user_id = db.add_user('test_user', 'test@example.com')
    print(f"   User created with ID: {user_id}")
    
    # Add some books
    print("\n2. Adding books...")
    book1 = db.add_book('Harry Potter', 'J.K. Rowling', 'Fantasy', 1997)
    book2 = db.add_book('1984', 'George Orwell', 'Fiction', 1949)
    print(f"   Added 2 books")
    
    # Get all books
    print("\n3. Getting all books...")
    books = db.get_all_books()
    for book in books:
        print(f"   - {book['title']} by {book['author']}")
    
    # Search books
    print("\n4. Searching for 'Harry'...")
    results = db.search_books('Harry')
    print(f"   Found {len(results)} book(s)")
    
    # Borrow a book
    print("\n5. Borrowing a book...")
    success = db.borrow_book(user_id, book1)
    print(f"   Borrowing {'successful' if success else 'failed'}")
    
    # Get statistics
    print("\n6. Library Statistics:")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    print("Test complete! Check 'test.db' file.")
    
    # Clean up
    os.remove('test.db')
