# member_example.py
from person_example import Person
from book_example import Book

class Member(Person):
    def __init__(self, name, age, member_id):
        super().__init__(name, age)
        self.member_id = member_id
        self.borrowed = []   # list of book titles

    def borrow_book(self, book):
        """Attempt to borrow a Book object; return True if success."""
        if book.lend():
            self.borrowed.append(book.title)
            return True
        return False

    def return_book(self, book_title, library_book_obj):
        """Return by title; requires a Book object reference to increment copy."""
        if book_title in self.borrowed:
            self.borrowed.remove(book_title)
            library_book_obj.receive()
            return True
        return False


if __name__ == "__main__":
    m = Member("Sara", 19, "M001")
    b = Book("Python 101", "Author", copies=1)
    print("Borrowed?", m.borrow_book(b))   # True
    print("Member borrowed list:", m.borrowed)
