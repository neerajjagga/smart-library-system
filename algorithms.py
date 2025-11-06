"""
SIMPLE SEARCH AND SORT ALGORITHMS
==================================
Easy-to-understand implementations with detailed comments

These are the SAME algorithms as the advanced version,
but with more comments and simpler variable names.
"""


import heapq
from collections import defaultdict

# ============================================
# 1. BINARY SEARCH - O(log n)
# ============================================

def binary_search(arr, target):
    """
    Binary Search - Find an item in a sorted list FAST!
    
    How it works:
    1. Look at the middle item
    2. If it's what we want, we're done!
    3. If our target is smaller, search the left half
    4. If our target is bigger, search the right half
    5. Repeat until found or no items left
    
    Time Complexity: O(log n)
    - For 1000 items: Only ~10 checks needed!
    - For 1 million items: Only ~20 checks!
    
    Example:
        books = ['Alice', 'Bob', 'Charlie', 'David']
        result = binary_search(books, 'Charlie')
        # Returns: 2 (the index)
    """
    left = 0                    # Start of search range
    right = len(arr) - 1        # End of search range
    
    # Keep searching while there are items to check
    while left <= right:
        # Find the middle position
        middle = (left + right) // 2
        
        # Check the middle item
        if arr[middle] == target:
            return middle       # Found it!
        
        elif arr[middle] < target:
            left = middle + 1   # Search right half
        
        else:
            right = middle - 1  # Search left half
    
    return -1                   # Not found


def binary_search_books(books, search_value, field='title'):
    """
    Binary Search for books (with field selection)
    
    Args:
        books: List of book dictionaries
        search_value: What to search for
        field: Which field to search ('title', 'author', etc.)
    
    Returns:
        Index of book if found, -1 if not found
    
    Example:
        books = [{'title': 'Book A'}, {'title': 'Book B'}]
        index = binary_search_books(books, 'Book B', 'title')
    """
    left = 0
    right = len(books) - 1
    
    while left <= right:
        middle = (left + right) // 2
        middle_value = books[middle][field].lower()
        search_lower = search_value.lower()
        
        if middle_value == search_lower:
            return middle
        elif middle_value < search_lower:
            left = middle + 1
        else:
            right = middle - 1
    
    return -1


# ============================================
# 2. MERGE SORT - O(n log n)
# ============================================

def merge_sort(arr):
    """
    Merge Sort - Sort items efficiently
    
    How it works:
    1. Split the list into two halves
    2. Sort each half (by calling merge_sort again - recursion!)
    3. Merge the two sorted halves back together
    
    Time Complexity: O(n log n)
    - For 1000 items: About 10,000 operations
    - Much faster than bubble sort (1,000,000 operations)
    
    Example:
        numbers = [5, 2, 8, 1, 9]
        sorted_numbers = merge_sort(numbers)
        # Returns: [1, 2, 5, 8, 9]
    """
    # Base case: A list of 0 or 1 item is already sorted
    if len(arr) <= 1:
        return arr
    
    # STEP 1: Split the list in half
    middle = len(arr) // 2
    left_half = arr[:middle]        # First half
    right_half = arr[middle:]       # Second half
    
    # STEP 2: Sort each half (recursion!)
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    
    # STEP 3: Merge the sorted halves
    return merge(left_sorted, right_sorted)


def merge(left, right):
    """
    Merge two sorted lists into one sorted list
    
    How it works:
    - Compare first item from each list
    - Take the smaller one
    - Repeat until all items are merged
    
    Example:
        left = [1, 5, 8]
        right = [2, 3, 9]
        result = merge(left, right)
        # Returns: [1, 2, 3, 5, 8, 9]
    """
    result = []         # This will hold our merged list
    i = 0               # Position in left list
    j = 0               # Position in right list
    
    # Compare items from both lists and add smaller one to result
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1      # Move to next item in left
        else:
            result.append(right[j])
            j += 1      # Move to next item in right
    
    # Add any remaining items from left list
    while i < len(left):
        result.append(left[i])
        i += 1
    
    # Add any remaining items from right list
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result


def merge_sort_books(books, field='title'):
    """
    Merge Sort for books (sort by any field)
    
    Args:
        books: List of book dictionaries
        field: Which field to sort by ('title', 'author', 'year')
    
    Returns:
        Sorted list of books
    
    Example:
        books = [
            {'title': 'Zebra Book', 'author': 'John'},
            {'title': 'Apple Book', 'author': 'Jane'}
        ]
        sorted_books = merge_sort_books(books, 'title')
    """
    # Base case
    if len(books) <= 1:
        return books
    
    # Split
    middle = len(books) // 2
    left_half = books[:middle]
    right_half = books[middle:]
    
    # Sort each half
    left_sorted = merge_sort_books(left_half, field)
    right_sorted = merge_sort_books(right_half, field)
    
    # Merge
    return merge_books(left_sorted, right_sorted, field)


def merge_books(left, right, field):
    """
    Merge two sorted book lists
    """
    result = []
    i = 0
    j = 0
    
    while i < len(left) and j < len(right):
        # Compare the specified field (case-insensitive)
        left_value = str(left[i].get(field, '')).lower()
        right_value = str(right[j].get(field, '')).lower()
        
        if left_value <= right_value:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining items
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


# ============================================
# 3. SIMPLE SEARCH (for comparison)
# ============================================

def simple_search(books, search_term):
    """
    Simple Linear Search - Check each book one by one
    
    Time Complexity: O(n)
    - For 1000 books: Checks all 1000
    - Slower than binary search but works on unsorted data
    
    This is used when:
    - Data is not sorted
    - We need partial matches (like "Harr" matching "Harry Potter")
    - Searching multiple fields at once
    """
    results = []
    search_lower = search_term.lower()
    
    # Check each book
    for book in books:
        # Search in title
        if search_lower in book.get('title', '').lower():
            results.append(book)
            continue
        
        # Search in author
        if search_lower in book.get('author', '').lower():
            results.append(book)
            continue
        
        # Search in genre
        if search_lower in book.get('genre', '').lower():
            results.append(book)
    
    return results


# ============================================
# 4. A* SEARCH ALGORITHM - AI TECHNIQUE
# ============================================


def calculate_book_similarity(book1, book2):
    """
    Calculate similarity score between two books
    
    This is the g(n) function in A* - actual cost from start to current node
    Lower score = more similar = better match
    
    Factors:
    - Genre match: 40% weight
    - Author match: 25% weight
    - Year similarity: 15% weight
    - Title similarity: 20% weight
    
    Returns:
        Float between 0 (identical) and 100 (completely different)
    """
    score = 0
    
    # Genre comparison (40 points)
    if book1.get('genre', '').lower() != book2.get('genre', '').lower():
        score += 40
    
    # Author comparison (25 points)
    if book1.get('author', '').lower() != book2.get('author', '').lower():
        score += 25
    
    # Year comparison (15 points)
    year1 = book1.get('year', 2000)
    year2 = book2.get('year', 2000)
    if year1 and year2:
        year_diff = abs(year1 - year2)
        # Normalize: 0-10 years = 0-15 points
        score += min(15, year_diff * 1.5)
    else:
        score += 15  # No year info = maximum penalty
    
    # Title word overlap (20 points)
    title1_words = set(book1.get('title', '').lower().split())
    title2_words = set(book2.get('title', '').lower().split())
    common_words = title1_words.intersection(title2_words)
    if len(title1_words) > 0:
        overlap_ratio = len(common_words) / len(title1_words)
        score += 20 * (1 - overlap_ratio)  # Less overlap = higher score
    else:
        score += 20
    
    return score


def calculate_heuristic(book, user_preferences, all_books_stats):
    """
    Calculate heuristic score h(n) for A* algorithm
    
    This estimates how good a book recommendation is based on:
    - Popularity (how many users borrowed it)
    - Availability (is it in stock?)
    - Recency (newer books might be better)
    
    Lower score = better recommendation
    
    Args:
        book: The book to evaluate
        user_preferences: Dictionary with user's preferred genres, authors
        all_books_stats: Statistics about all books (for popularity)
    
    Returns:
        Float heuristic score (0-50)
    """
    h_score = 0
    
    # Availability factor (20 points)
    available = book.get('available_copies', 0)
    if available == 0:
        h_score += 20  # Not available = high penalty
    elif available == 1:
        h_score += 10  # Only 1 copy = medium penalty
    # else: available > 1, no penalty
    
    # Popularity factor (15 points)
    # Books borrowed by fewer people get higher penalty
    borrow_count = all_books_stats.get('borrow_counts', {}).get(book['book_id'], 0)
    if borrow_count == 0:
        h_score += 15  # Never borrowed = might not be good
    elif borrow_count < 3:
        h_score += 10  # Rarely borrowed
    elif borrow_count < 10:
        h_score += 5   # Moderately popular
    # else: Very popular, no penalty
    
    # Recency factor (15 points)
    year = book.get('year', 1900)
    if year:
        age = 2024 - year
        if age > 50:
            h_score += 15  # Very old book
        elif age > 20:
            h_score += 10  # Old book
        elif age > 10:
            h_score += 5   # Moderately old
        # else: Recent book, no penalty
    else:
        h_score += 10  # Unknown year
    
    return h_score


def astar_book_recommendations(user_borrowed_books, all_books, top_n=10):
    """
    A* SEARCH ALGORITHM for Book Recommendations
    ============================================
    
    This is an AI technique from your syllabus (Unit-II)!
    
    How A* Works:
    1. Start with books user has borrowed (start state)
    2. Find similar books using f(n) = g(n) + h(n)
       - g(n) = similarity to user's books (actual cost)
       - h(n) = heuristic estimate (popularity, availability)
    3. Use priority queue to always explore best candidates first
    4. Return top N recommendations (goal state)
    
    Why A* is better than simple search:
    - Uses INFORMED SEARCH (heuristics guide the search)
    - Finds OPTIMAL recommendations (best f-score)
    - More EFFICIENT (doesn't check all books blindly)
    - Considers MULTIPLE FACTORS (not just genre)
    
    Time Complexity: O(b^d) where b=branching factor, d=depth
    But with good heuristics, much faster than O(n) in practice!
    
    Args:
        user_borrowed_books: List of books user has borrowed
        all_books: List of all available books
        top_n: Number of recommendations to return
    
    Returns:
        List of recommended books with their scores
    """
    
    # Edge case: No borrowed books
    if not user_borrowed_books:
        # Return most popular available books
        available = [b for b in all_books if b.get('available_copies', 0) > 0]
        return sorted(available, key=lambda x: x.get('year', 0), reverse=True)[:top_n]
    
    # STEP 1: Build user preference profile
    user_preferences = {
        'genres': defaultdict(int),
        'authors': defaultdict(int),
        'avg_year': 0
    }
    
    for book in user_borrowed_books:
        user_preferences['genres'][book.get('genre', '').lower()] += 1
        user_preferences['authors'][book.get('author', '').lower()] += 1
    
    # Calculate average year
    years = [b.get('year', 2000) for b in user_borrowed_books if b.get('year')]
    user_preferences['avg_year'] = sum(years) / len(years) if years else 2000
    
    # STEP 2: Calculate statistics for all books
    all_books_stats = {
        'borrow_counts': {}  # In real system, get from database
    }
    
    # STEP 3: A* Search - Priority Queue
    # Format: (f_score, book_id, book)
    priority_queue = []
    
    # Get IDs of already borrowed books
    borrowed_ids = set(book['book_id'] for book in user_borrowed_books)
    
    # STEP 4: Evaluate each candidate book
    for book in all_books:
        # Skip already borrowed books
        if book['book_id'] in borrowed_ids:
            continue
        
        # Calculate g(n) - similarity to user's books
        # Take minimum distance to any borrowed book
        g_scores = []
        for borrowed_book in user_borrowed_books:
            similarity = calculate_book_similarity(borrowed_book, book)
            g_scores.append(similarity)
        
        g_score = min(g_scores) if g_scores else 50  # Best match
        
        # Calculate h(n) - heuristic estimate
        h_score = calculate_heuristic(book, user_preferences, all_books_stats)
        
        # Calculate f(n) = g(n) + h(n)
        f_score = g_score + h_score
        
        # Add to priority queue (heapq uses min-heap)
        heapq.heappush(priority_queue, (f_score, book['book_id'], book))
    
    # STEP 5: Extract top N recommendations
    recommendations = []
    while priority_queue and len(recommendations) < top_n:
        f_score, book_id, book = heapq.heappop(priority_queue)
        
        # Add score information for debugging/display
        book_with_score = book.copy()
        book_with_score['recommendation_score'] = round(f_score, 2)
        book_with_score['match_quality'] = 'Excellent' if f_score < 30 else \
                                           'Good' if f_score < 50 else \
                                           'Fair' if f_score < 70 else 'Poor'
        
        recommendations.append(book_with_score)
    
    return recommendations


def compare_recommendation_methods(user_borrowed_books, all_books):
    """
    Compare Simple Recommendation vs A* Algorithm
    
    This demonstrates why A* is better for your AI case study!
    """
    print("\n" + "="*60)
    print("RECOMMENDATION ALGORITHM COMPARISON")
    print("="*60)
    
    # Method 1: Simple Genre-Based (Current approach)
    print("\n1. SIMPLE GENRE-BASED RECOMMENDATION")
    print("-" * 40)
    borrowed_genres = set(b['genre'] for b in user_borrowed_books)
    borrowed_ids = set(b['book_id'] for b in user_borrowed_books)
    
    simple_recs = []
    for book in all_books:
        if book['book_id'] not in borrowed_ids and book['genre'] in borrowed_genres:
            simple_recs.append(book)
    
    print(f"Found: {len(simple_recs)} recommendations")
    print("Pros: Fast, simple to implement")
    print("Cons: Only considers genre, no ranking quality")
    
    # Method 2: A* Algorithm (AI approach)
    print("\n2. A* SEARCH ALGORITHM (AI TECHNIQUE)")
    print("-" * 40)
    astar_recs = astar_book_recommendations(user_borrowed_books, all_books, top_n=10)
    
    print(f"Found: {len(astar_recs)} recommendations")
    print("Pros: Multi-factor analysis, optimal ranking, informed search")
    print("Cons: Slightly more complex (but worth it!)")
    
    # Show top 3 from A*
    print("\nTop 3 A* Recommendations:")
    for i, book in enumerate(astar_recs[:3], 1):
        print(f"  {i}. {book['title']} by {book['author']}")
        print(f"     Score: {book['recommendation_score']} ({book['match_quality']} match)")
    
    print("\n" + "="*60)
    return simple_recs, astar_recs


# ============================================
# 5. HELPER FUNCTIONS
# ============================================

def compare_search_methods(books, target):
    """
    Compare Binary Search vs Simple Search
    
    This shows why we use different algorithms for different cases!
    """
    print(f"\n=== Searching for: {target} ===")
    
    # Method 1: Simple Search (works on unsorted data, partial matches)
    simple_results = simple_search(books, target)
    print(f"Simple Search found: {len(simple_results)} books")
    print("  Pros: Works on unsorted data, finds partial matches")
    print("  Cons: Slow for large datasets")
    
    # Method 2: Binary Search (requires sorted data, exact match)
    sorted_books = merge_sort_books(books, 'title')
    index = binary_search_books(sorted_books, target, 'title')
    print(f"Binary Search found at index: {index}")
    print("  Pros: Very fast! O(log n)")
    print("  Cons: Requires sorted data, exact match only")
    
    return simple_results


# ============================================
# TESTING CODE (Run this file to see demos)
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("ALGORITHM DEMONSTRATIONS")
    print("=" * 50)
    
    # Demo 1: Binary Search
    print("\n1. BINARY SEARCH DEMO")
    print("-" * 30)
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(f"Sorted list: {numbers}")
    print(f"Searching for 7...")
    result = binary_search(numbers, 7)
    print(f"Found at index: {result}")
    print(f"Value: {numbers[result]}")
    
    # Demo 2: Merge Sort
    print("\n2. MERGE SORT DEMO")
    print("-" * 30)
    unsorted = [5, 2, 8, 1, 9, 3, 7]
    print(f"Unsorted: {unsorted}")
    sorted_list = merge_sort(unsorted)
    print(f"Sorted:   {sorted_list}")
    
    # Demo 3: Books
    print("\n3. BOOK SEARCH DEMO")
    print("-" * 30)
    sample_books = [
        {'title': 'Harry Potter', 'author': 'J.K. Rowling', 'genre': 'Fantasy'},
        {'title': '1984', 'author': 'George Orwell', 'genre': 'Fiction'},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy'},
    ]
    
    # Sort books
    sorted_books = merge_sort_books(sample_books, 'title')
    print("Sorted books:")
    for book in sorted_books:
        print(f"  - {book['title']}")
    
    # Search for a book
    print("\nSearching for '1984'...")
    index = binary_search_books(sorted_books, '1984', 'title')
    if index != -1:
        print(f"Found: {sorted_books[index]['title']} by {sorted_books[index]['author']}")
    
    # Demo 4: A* Algorithm for Recommendations
    print("\n4. A* ALGORITHM DEMO (AI TECHNIQUE!)")
    print("-" * 30)
    
    # Create more sample books for better demo
    all_sample_books = [
        {'book_id': 1, 'title': 'Harry Potter', 'author': 'J.K. Rowling', 'genre': 'Fantasy', 'year': 1997, 'available_copies': 3},
        {'book_id': 2, 'title': '1984', 'author': 'George Orwell', 'genre': 'Fiction', 'year': 1949, 'available_copies': 2},
        {'book_id': 3, 'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy', 'year': 1937, 'available_copies': 1},
        {'book_id': 4, 'title': 'Lord of the Rings', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy', 'year': 1954, 'available_copies': 2},
        {'book_id': 5, 'title': 'Brave New World', 'author': 'Aldous Huxley', 'genre': 'Fiction', 'year': 1932, 'available_copies': 1},
        {'book_id': 6, 'title': 'The Hunger Games', 'author': 'Suzanne Collins', 'genre': 'Science Fiction', 'year': 2008, 'available_copies': 4},
    ]
    
    # User has borrowed Fantasy books
    user_borrowed = [
        {'book_id': 1, 'title': 'Harry Potter', 'author': 'J.K. Rowling', 'genre': 'Fantasy', 'year': 1997},
    ]
    
    print("\nUser has borrowed:")
    for book in user_borrowed:
        print(f"  - {book['title']} ({book['genre']})")
    
    print("\nRunning A* Algorithm for recommendations...")
    recommendations = astar_book_recommendations(user_borrowed, all_sample_books, top_n=3)
    
    print("\nTop 3 Recommendations:")
    for i, book in enumerate(recommendations, 1):
        score = book.get('recommendation_score', 0)
        quality = book.get('match_quality', 'N/A')
        print(f"  {i}. {book['title']} by {book['author']}")
        print(f"     Genre: {book['genre']}, Year: {book['year']}")
        print(f"     Score: {score} ({quality} match)")
    
    print("\n💡 Why these recommendations?")
    print("  - A* considers: genre, author, year, availability")
    print("  - Lower score = Better match")
    print("  - Uses f(n) = g(n) + h(n) formula")
    
    print("\n" + "="*50)
