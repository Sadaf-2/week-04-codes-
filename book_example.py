# book_example.py
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


if __name__ == "__main__":
    b = Book("1984", "Orwell", copies=2)
    print(b.available())        # True
    print("lend:", b.lend())    # True -> copies becomes 1
    print("copies left:", b.copies)
