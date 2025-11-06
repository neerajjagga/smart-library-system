"""
ADD SAMPLE DATA
===============
This script adds sample books and users to the database

Run this once to populate your library with test data!
"""

from database import SimpleDatabase

def add_sample_data():
    """
    Add sample books and users to the database
    """
    print("=" * 60)
    print("ADDING SAMPLE DATA TO LIBRARY")
    print("=" * 60)
    
    # Create database
    db = SimpleDatabase()
    
    # STEP 1: Add users
    print("\n📝 Adding users...")
    users = [
        ('john_doe', 'john@example.com'),
        ('jane_smith', 'jane@example.com'),
        ('alice_wonder', 'alice@example.com'),
    ]
    
    user_ids = []
    for username, email in users:
        user_id = db.add_user(username, email)
        if user_id:
            print(f"   ✓ {username}")
            user_ids.append(user_id)
        else:
            print(f"   ✗ {username} (already exists)")
    
    # STEP 2: Add books
    print("\n📚 Adding books...")
    books = [
        ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, 
         'A gripping tale of racial injustice and childhood innocence.'),
        
        ('1984', 'George Orwell', 'Science Fiction', 1949,
         'A dystopian novel about totalitarianism and surveillance.'),
        
        ('Pride and Prejudice', 'Jane Austen', 'Romance', 1813,
         'A romantic novel of manners in 19th century England.'),
        
        ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925,
         'A novel about the American Dream and the Jazz Age.'),
        
        ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 'Fantasy', 1997,
         'A young wizard\'s journey begins at Hogwarts.'),
        
        ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937,
         'The quest of hobbit Bilbo Baggins and his adventures.'),
        
        ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 1951,
         'A story about teenage rebellion and alienation.'),
        
        ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954,
         'An epic quest to destroy the One Ring.'),
        
        ('Brave New World', 'Aldous Huxley', 'Science Fiction', 1932,
         'A dystopian novel about a futuristic World State.'),
        
        ('The Hunger Games', 'Suzanne Collins', 'Science Fiction', 2008,
         'A dystopian novel about a televised fight to the death.'),
        
        ('Dune', 'Frank Herbert', 'Science Fiction', 1965,
         'Politics, religion, and ecology on the desert planet Arrakis.'),
        
        ('The Da Vinci Code', 'Dan Brown', 'Mystery', 2003,
         'A mystery thriller following symbologist Robert Langdon.'),
        
        ('The Alchemist', 'Paulo Coelho', 'Fiction', 1988,
         'A philosophical book about following one\'s dreams.'),
        
        ('Sapiens', 'Yuval Noah Harari', 'Non-Fiction', 2011,
         'A brief history of humankind and civilization.'),
        
        ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery', 2005,
         'A psychological thriller about investigation and mystery.'),
    ]
    
    book_ids = []
    for title, author, genre, year, description in books:
        book_id = db.add_book(title, author, genre, year, description, copies=2)
        print(f"   ✓ {title}")
        book_ids.append(book_id)
    
    # STEP 3: Add some borrowing records (so recommendations work)
    print("\n📖 Creating borrowing history...")
    if user_ids and book_ids:
        # User 1 borrows Fantasy books
        db.borrow_book(user_ids[0], book_ids[4])  # Harry Potter
        db.borrow_book(user_ids[0], book_ids[5])  # The Hobbit
        print(f"   ✓ User 1 borrowed 2 books")
        
        # User 2 borrows Fiction books
        db.borrow_book(user_ids[1], book_ids[0])  # To Kill a Mockingbird
        db.borrow_book(user_ids[1], book_ids[3])  # The Great Gatsby
        print(f"   ✓ User 2 borrowed 2 books")
        
        # User 3 borrows Sci-Fi books
        db.borrow_book(user_ids[2], book_ids[1])  # 1984
        db.borrow_book(user_ids[2], book_ids[8])  # Brave New World
        print(f"   ✓ User 3 borrowed 2 books")
    
    # STEP 4: Show statistics
    print("\n📊 Library Statistics:")
    stats = db.get_stats()
    print(f"   Total Books: {stats['total_books']}")
    print(f"   Available: {stats['available_books']}")
    print(f"   Borrowed: {stats['borrowed_books']}")
    print(f"   Users: {stats['total_users']}")
    
    print("\n" + "=" * 60)
    print("✅ SAMPLE DATA ADDED SUCCESSFULLY!")
    print("\nYou can now run: python app.py")
    print("=" * 60)


if __name__ == '__main__':
    add_sample_data()
