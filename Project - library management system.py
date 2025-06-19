import datetime

# --- Book Class ---
class Book:
    """Represents a single book."""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def borrow(self) -> bool:
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False

    def return_book(self) -> bool:
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False

    def __str__(self) -> str:
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"

# --- User Class ---
class User:
    """Represents a library user."""
    def __init__(self, name: str, user_id: str):
        self.name = name
        self.user_id = user_id
        self.borrowed_books_isbns = [] # Stores ISBNs of borrowed books

    def add_borrowed_book_isbn(self, isbn: str) -> None:
        if isbn not in self.borrowed_books_isbns:
            self.borrowed_books_isbns.append(isbn)

    def remove_borrowed_book_isbn(self, isbn: str) -> None:
        if isbn in self.borrowed_books_isbns:
            self.borrowed_books_isbns.remove(isbn)

    def __str__(self) -> str:
        return f"User: {self.name} (ID: {self.user_id}), Borrowed: {len(self.borrowed_books_isbns)} books"

# --- Library Class ---
class Library:
    """Manages books and users."""
    def __init__(self):
        self.books: dict[str, Book] = {}  # ISBN -> Book object
        self.users: dict[str, User] = {}  # User ID -> User object

    def add_book(self, book: Book) -> bool:
        if book.isbn in self.books:
            print(f"Error: Book with ISBN {book.isbn} already exists.")
            return False
        self.books[book.isbn] = book
        print(f"Book '{book.title}' added.")
        return True

    def remove_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            print(f"Error: Book with ISBN {isbn} not found.")
            return False
        if self.books[isbn].is_borrowed:
            print(f"Error: Book '{self.books[isbn].title}' is borrowed.")
            return False
        del self.books[isbn]
        print(f"Book with ISBN {isbn} removed.")
        return True

    def register_user(self, user: User) -> bool:
        if user.user_id in self.users:
            print(f"Error: User with ID {user.user_id} already exists.")
            return False
        self.users[user.user_id] = user
        print(f"User '{user.name}' registered.")
        return True

    def remove_user(self, user_id: str) -> bool:
        if user_id not in self.users:
            print(f"Error: User with ID {user_id} not found.")
            return False
        if self.users[user_id].borrowed_books_isbns:
            print(f"Error: User '{self.users[user_id].name}' has borrowed books.")
            return False
        del self.users[user_id]
        print(f"User with ID {user_id} removed.")
        return True

    def borrow_book(self, isbn: str, user_id: str) -> bool:
        book = self.books.get(isbn)
        user = self.users.get(user_id)
        if not book:
            print(f"Error: Book with ISBN {isbn} not found.")
            return False
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return False
        if book.is_borrowed:
            print(f"Error: Book '{book.title}' is already borrowed.")
            return False

        if book.borrow():
            user.add_borrowed_book_isbn(isbn)
            print(f"Book '{book.title}' borrowed by '{user.name}'.")
            return True
        return False

    def return_book(self, isbn: str, user_id: str) -> bool:
        book = self.books.get(isbn)
        user = self.users.get(user_id)
        if not book:
            print(f"Error: Book with ISBN {isbn} not found.")
            return False
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return False
        if isbn not in user.borrowed_books_isbns:
            print(f"Error: User '{user.name}' did not borrow '{book.title}'.")
            return False

        if book.return_book():
            user.remove_borrowed_book_isbn(isbn)
            print(f"Book '{book.title}' returned by '{user.name}'.")
            return True
        return False

    def search_book(self, query: str) -> list[Book]:
        found = []
        q_lower = query.lower()
        for book in self.books.values():
            if (q_lower in book.title.lower() or
                q_lower in book.author.lower() or
                q_lower == book.isbn.lower()):
                found.append(book)
        return found

    def display_all_books(self) -> None:
        print("\n--- All Books ---")
        if not self.books:
            print("No books in library.")
            return
        for book in self.books.values():
            print(book)

    def display_all_users(self) -> None:
        print("\n--- All Users ---")
        if not self.users:
            print("No users registered.")
            return
        for user in self.users.values():
            print(user)

    def display_user_borrowed_books(self, user_id: str) -> None:
        user = self.users.get(user_id)
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return
        print(f"\n--- Books Borrowed by {user.name} ---")
        if not user.borrowed_books_isbns:
            print("No books borrowed by this user.")
            return
        for isbn in user.borrowed_books_isbns:
            book = self.books.get(isbn)
            if book:
                print(book)
            else:
                print(f"Book (ISBN: {isbn}) not found in library.")

# --- Console Interface ---
def main():
    lib = Library()

    while True:
        print("\n--- Menu ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Register User")
        print("4. Remove User")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Search Book")
        print("8. Display All Books")
        print("9. Display All Users")
        print("10. Display User Borrowed Books")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            lib.add_book(Book(title, author, isbn))
        elif choice == '2':
            isbn = input("ISBN to remove: ")
            lib.remove_book(isbn)
        elif choice == '3':
            name = input("User Name: ")
            user_id = input("User ID: ")
            lib.register_user(User(name, user_id))
        elif choice == '4':
            user_id = input("User ID to remove: ")
            lib.remove_user(user_id)
        elif choice == '5':
            isbn = input("Book ISBN: ")
            user_id = input("User ID: ")
            lib.borrow_book(isbn, user_id)
        elif choice == '6':
            isbn = input("Book ISBN: ")
            user_id = input("User ID: ")
            lib.return_book(isbn, user_id)
        elif choice == '7':
            query = input("Search (title/author/ISBN): ")
            found = lib.search_book(query)
            if found:
                print("--- Found Books ---")
                for book in found:
                    print(book)
            else:
                print("No books found.")
        elif choice == '8':
            lib.display_all_books()
        elif choice == '9':
            lib.display_all_users()
        elif choice == '10':
            user_id = input("User ID: ")
            lib.display_user_borrowed_books(user_id)
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
