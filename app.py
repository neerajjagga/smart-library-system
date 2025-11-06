"""
SIMPLE LIBRARY SYSTEM - Flask Application
==========================================
Easy-to-understand web application for managing books

This uses the SAME algorithms (Binary Search & Merge Sort)
but with clearer code and more comments!
"""

from flask import Flask, render_template, request, redirect, url_for, session
from database import SimpleDatabase
from algorithms import merge_sort_books, simple_search

# Create Flask app
app = Flask(__name__)
app.secret_key = 'simple-library-secret-key'

# Create database connection
db = SimpleDatabase()


# ============================================
# HOME PAGE
# ============================================

@app.route('/')
def index():
    """
    Home page - Shows statistics and recent books
    
    What happens here:
    1. Get library statistics (total books, users, etc.)
    2. Get all books from database
    3. Sort them by title using MERGE SORT
    4. Show the first 6 books
    """
    # Get statistics
    stats = db.get_stats()
    
    # Get all books
    all_books = db.get_all_books()
    
    # Sort books by title using MERGE SORT (O(n log n))
    sorted_books = merge_sort_books(all_books, field='title')
    
    # Take first 6 books to show on home page
    recent_books = sorted_books[:6]
    
    return render_template('index.html', 
                         stats=stats, 
                         recent_books=recent_books,
                         popular_books=[])  # Keep template compatible


# ============================================
# SEARCH PAGE
# ============================================

@app.route('/search')
def search():
    """
    Search for books
    
    How it works:
    1. Get search query from user
    2. Use SIMPLE SEARCH to find matching books
       (checks title, author, genre - allows partial matches)
    3. Sort results using MERGE SORT
    4. Show results
    
    Note: We use simple search here (not binary search) because:
    - We need partial matches ("Harr" matches "Harry Potter")
    - We search multiple fields (title, author, genre)
    - Binary search only works for exact matches on sorted data
    """
    # Get search term from URL (?q=something)
    query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'relevance')
    
    if not query:
        return render_template('search.html', books=[], query='')
    
    # STEP 1: Search for books using simple search
    # This checks title, author, and genre for matches
    results = simple_search(db.get_all_books(), query)
    
    # STEP 2: Sort results using MERGE SORT
    if sort_by == 'title':
        results = merge_sort_books(results, field='title')
    elif sort_by == 'author':
        results = merge_sort_books(results, field='author')
    elif sort_by == 'year':
        # Sort by year, newest first (reverse order)
        results = merge_sort_books(results, field='year')
        results.reverse()
    
    # Get unique genres for filter dropdown
    all_books = db.get_all_books()
    genres = sorted(list(set(book['genre'] for book in all_books if book.get('genre'))))
    
    return render_template('search.html', 
                         books=results, 
                         query=query,
                         sort_by=sort_by,
                         genres=genres,
                         filter_genre='')


# ============================================
# BOOK DETAIL PAGE
# ============================================

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """
    Show details of a specific book
    
    What we do:
    1. Get the book from database
    2. Find similar books (same genre)
    3. Show book details and recommendations
    """
    # Get the book
    book = db.get_book_by_id(book_id)
    
    if not book:
        return "Book not found", 404
    
    # Find similar books (same genre)
    # This is a simple recommendation system
    all_books = db.get_all_books()
    recommendations = []
    
    for other_book in all_books:
        # Skip the current book
        if other_book['book_id'] == book_id:
            continue
        
        # If same genre, add to recommendations
        if other_book['genre'] == book['genre']:
            recommendations.append(other_book)
        
        # Limit to 5 recommendations
        if len(recommendations) >= 5:
            break
    
    # Check if user borrowed this book
    user_id = session.get('user_id', 1)  # Default user for demo
    borrowed_books = db.get_user_borrowed_books(user_id)
    currently_borrowed = any(
        b['book_id'] == book_id and b['status'] == 'borrowed' 
        for b in borrowed_books
    )
    
    return render_template('book_detail.html', 
                         book=book, 
                         recommendations=recommendations,
                         currently_borrowed=currently_borrowed)


# ============================================
# ALL BOOKS PAGE
# ============================================

@app.route('/books')
def all_books():
    """
    Show all books with sorting options
    
    Demonstrates MERGE SORT on different fields
    """
    sort_by = request.args.get('sort', 'title')
    genre_filter = request.args.get('genre', '')
    
    # Get all books
    books = db.get_all_books()
    
    # Filter by genre if selected
    if genre_filter:
        books = [book for book in books if book.get('genre', '').lower() == genre_filter.lower()]
    
    # Sort using MERGE SORT (O(n log n))
    if sort_by == 'title':
        books = merge_sort_books(books, field='title')
    elif sort_by == 'author':
        books = merge_sort_books(books, field='author')
    elif sort_by == 'year':
        books = merge_sort_books(books, field='year')
        books.reverse()  # Newest first
    elif sort_by == 'genre':
        books = merge_sort_books(books, field='genre')
    
    # Get all genres for filter
    all_books = db.get_all_books()
    genres = sorted(list(set(book['genre'] for book in all_books if book.get('genre'))))
    
    return render_template('all_books.html', 
                         books=books, 
                         sort_by=sort_by,
                         genres=genres,
                         genre_filter=genre_filter)


# ============================================
# RECOMMENDATIONS PAGE
# ============================================

@app.route('/recommendations')
def recommendations():
    """
    Show personalized recommendations
    
    Simple recommendation logic:
    - Find books user has borrowed
    - Recommend books from same genres
    """
    user_id = session.get('user_id', 1)
    
    # Get user's borrowed books
    borrowed = db.get_user_borrowed_books(user_id)
    borrowed_genres = set(b['genre'] for b in borrowed)
    borrowed_ids = set(b['book_id'] for b in borrowed)
    
    # Find books from same genres
    all_books = db.get_all_books()
    recommendations_list = []
    
    for book in all_books:
        # Skip if already borrowed
        if book['book_id'] in borrowed_ids:
            continue
        
        # If book is in a genre user likes, recommend it
        if book['genre'] in borrowed_genres:
            recommendations_list.append(book)
    
    # Sort recommendations
    recommendations_list = merge_sort_books(recommendations_list, field='title')
    
    return render_template('recommendations.html', 
                         collaborative_recommendations=recommendations_list[:10],
                         popular_books=[])


# ============================================
# MY BOOKS PAGE
# ============================================

@app.route('/my-books')
def my_books():
    """
    Show user's borrowed books
    """
    user_id = session.get('user_id', 1)
    
    # Get all borrowings for this user
    borrowed = db.get_user_borrowed_books(user_id)
    
    # Get full book details for each borrowing
    borrowed_books = []
    for borrow_record in borrowed:
        book = db.get_book_by_id(borrow_record['book_id'])
        if book:
            book['borrow_info'] = borrow_record
            borrowed_books.append(book)
    
    return render_template('my_books.html', borrowed_books=borrowed_books)


# ============================================
# BORROW & RETURN ACTIONS
# ============================================

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    """
    Borrow a book
    
    Steps:
    1. Get current user
    2. Try to borrow the book
    3. Redirect back to book page
    """
    user_id = session.get('user_id', 1)
    
    # Try to borrow
    success = db.borrow_book(user_id, book_id)
    
    if success:
        return redirect(url_for('book_detail', book_id=book_id))
    else:
        return "Book not available", 400


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    """
    Return a borrowed book
    """
    success = db.return_book(borrow_id)
    
    if success:
        return redirect(url_for('my_books'))
    else:
        return "Error returning book", 400


# ============================================
# ADD BOOK (Admin)
# ============================================

@app.route('/admin/add-book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the library
    """
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        year = request.form.get('publication_year')
        description = request.form.get('description')
        copies = request.form.get('total_copies', 1)
        
        # Add book to database
        book_id = db.add_book(
            title=title,
            author=author,
            genre=genre,
            year=int(year) if year else None,
            description=description,
            copies=int(copies)
        )
        
        return redirect(url_for('book_detail', book_id=book_id))
    
    return render_template('add_book.html')


# ============================================
# API ENDPOINTS (for AJAX)
# ============================================

@app.route('/api/search')
def api_search():
    """
    API endpoint for quick search (used by JavaScript)
    """
    query = request.args.get('q', '').strip()
    
    if not query:
        return {'results': []}
    
    # Search and return top 10 results
    results = simple_search(db.get_all_books(), query)
    return {'results': results[:10]}


# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("SIMPLE LIBRARY SYSTEM")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, port=5000)
