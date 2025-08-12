# person_example.py
class Person:
    def __init__(self, name, age):
        # attributes
        self.name = name
        self.age = age

    # method
    def greet(self):
        print(f"Hi, I'm {self.name} ({self.age} yrs).")

    def is_adult(self):
        return self.age >= 18


if __name__ == "__main__":
    p = Person("Ali", 21)
    p.greet()  # Hi, I'm Ali (21 yrs).
    print("Adult?", p.is_adult())
