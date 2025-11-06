"""
SIMPLE SEARCH AND SORT ALGORITHMS
==================================
Easy-to-understand implementations with detailed comments

These are the SAME algorithms as the advanced version,
but with more comments and simpler variable names.
"""

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
# 4. HELPER FUNCTIONS
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
    
    print("\n" + "=" * 50)
