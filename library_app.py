# library_app.py
from datetime import datetime

# ----- Book -----
class Book:
    def __init__(self, title, author, copies=1):
        self.title = title
        self.author = author
        self.copies = max(0, int(copies))

    def available(self):
        return self.copies > 0

    def lend(self):
        if self.available():
            self.copies -= 1
            return True
        return False

    def receive(self):
        self.copies += 1

    def __repr__(self):
        return f"<Book: {self.title} by {self.author} | copies={self.copies}>"


# ----- Person (base) -----
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = int(age)


# ----- Member (inherits Person) -----
class Member(Person):
    def __init__(self, name, age, member_id):
        super().__init__(name, age)
        self.member_id = member_id
        self.borrowed = []  # list of (title, borrowed_date)

    def borrow(self, book_obj):
        if book_obj.lend():
            self.borrowed.append((book_obj.title, datetime.now().date().isoformat()))
            return True
        return False

    def return_book(self, title):
        for i, (t, _) in enumerate(self.borrowed):
            if t == title:
                self.borrowed.pop(i)
                return True
        return False

    def __repr__(self):
        return f"<Member {self.member_id}: {self.name}, borrowed={len(self.borrowed)}>"


# ----- Library (composition) -----
class Library:
    def __init__(self):
        self.books = {}    # title -> Book
        self.members = {}  # member_id -> Member

    # Books
    def add_book(self, title, author, copies=1):
        if title in self.books:
            self.books[title].copies += int(copies)
        else:
            self.books[title] = Book(title, author, copies)
        return self.books[title]

    def list_books(self):
        if not self.books:
            print("No books in library.")
            return
        for b in self.books.values():
            print(f"- {b.title} by {b.author} (copies: {b.copies})")

    # Members
    def register_member(self, name, age, member_id=None):
        if member_id is None:
            member_id = f"M{len(self.members)+1:03d}"
        if member_id in self.members:
            raise ValueError("Member ID already exists")
        m = Member(name, age, member_id)
        self.members[member_id] = m
        return m

    def list_members(self):
        if not self.members:
            print("No registered members.")
            return
        for m in self.members.values():
            borrowed_titles = [t for t, _ in m.borrowed]
            print(f"- {m.member_id}: {m.name} (age {m.age}) | borrowed: {borrowed_titles}")

    # Lend / Return
    def lend_book(self, title, member_id):
        if title not in self.books:
            return False, "Book not found"
        if member_id not in self.members:
            return False, "Member not found"
        book = self.books[title]
        member = self.members[member_id]
        if member.borrow(book):
            return True, "Book lent successfully"
        return False, "No copies available"

    def return_book(self, title, member_id):
        if member_id not in self.members:
            return False, "Member not found"
        if title not in self.books:
            return False, "Book not found in library records"
        member = self.members[member_id]
        if not member.return_book(title):
            return False, "Member did not borrow this book"
        self.books[title].receive()
        return True, "Book returned successfully"


# ----- CLI -----
def main():
    lib = Library()
    lib.add_book("1984", "George Orwell", copies=2)
    lib.add_book("Python 101", "Jane Doe", copies=1)
    lib.register_member("Ali", 21, "M001")
    lib.register_member("Sara", 19, "M002")

    MENU = """\nLibrary Menu:
1) Add Book
2) Register Member
3) Lend Book
4) Return Book
5) List Books
6) List Members
7) Exit
Enter choice: """

    while True:
        choice = input(MENU).strip()
        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            copies = input("Copies (default 1): ").strip() or "1"
            lib.add_book(title, author, copies)
            print("Book added/updated.")
        elif choice == "2":
            name = input("Member name: ").strip()
            age = input("Age: ").strip()
            try:
                member = lib.register_member(name, age)
                print(f"Registered with ID {member.member_id}")
            except ValueError as e:
                print("Error:", e)
        elif choice == "3":
            title = input("Book title to lend: ").strip()
            member_id = input("Member ID: ").strip()
            ok, msg = lib.lend_book(title, member_id)
            print(msg)
        elif choice == "4":
            title = input("Book title to return: ").strip()
            member_id = input("Member ID: ").strip()
            ok, msg = lib.return_book(title, member_id)
            print(msg)
        elif choice == "5":
            lib.list_books()
        elif choice == "6":
            lib.list_members()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
