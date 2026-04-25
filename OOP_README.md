# 🏛️ The Pillars of Object-Oriented Programming (OOP)

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects," which can contain data (fields/attributes) and code (methods/functions). While there are often four core principles discussed, many developers focus on these **three fundamental pillars** that form the backbone of modern software design.

---

## 1. 📦 Encapsulation
**"Keep it private, keep it safe."**

Encapsulation is the practice of bundling data and the methods that operate on that data into a single unit (a class). It also involves **restricting direct access** to some of an object's components, which is a means of preventing accidental interference and misuse of the data.

### Key Benefits:
- **Data Hiding:** Protecting the internal state of an object.
- **Control:** You decide how the data is accessed or modified (using getters and setters).
- **Flexibility:** You can change the internal implementation without affecting the code that uses the object.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}")

    def get_balance(self):
        return self.__balance
```

---

## 2. 🌳 Inheritance
**"Don't reinvent the wheel."**

Inheritance allows a class (child/subclass) to acquire the properties and behaviors of another class (parent/superclass). It promotes **code reusability** and establishes a natural hierarchy between objects.

### Key Benefits:
- **Reusability:** Use existing code to create new classes.
- **Organization:** Create a logical "is-a" relationship (e.g., a `Dog` **is a** `Animal`).
- **Maintainability:** Fix a bug in the parent class, and it's fixed in all children.

```python
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):  # Dog inherits from Animal
    def speak(self):
        print("Woof! Woof!")

my_dog = Dog()
my_dog.speak()  # Output: Woof! Woof!
```

---

## 3. 🎭 Polymorphism
**"One interface, many forms."**

Polymorphism allows objects of different classes to be treated as objects of a common superclass. The most common form is when a child class overrides a method of its parent. It allows one function to behave differently based on the object it is acting upon.

### Key Benefits:
- **Flexibility:** Write code that can work with different types of objects.
- **Interchangeability:** Swap out implementations without changing the calling code.
- **Simplicity:** Reduces the need for complex conditional logic (if/else).

```python
animals = [Dog(), Animal()]

for animal in animals:
    animal.speak() 
    # The same call produces different results!
```

---

> [!NOTE]
> ### 💡 What about Abstraction?
> Although often cited as the **4th Pillar**, Abstraction is frequently grouped with Encapsulation. Abstraction focuses on **hiding the complexity** and only showing the essential features of an object. It's the concept of "what it does" versus "how it does it."

---

### 🚀 Summary
| Pillar | Purpose | Keyword |
| :--- | :--- | :--- |
| **Encapsulation** | Security & Organization | *Private* |
| **Inheritance** | Code Reusability | *Hierarchy* |
| **Polymorphism** | Flexibility | *Override* |

Happy Coding! 💻✨
