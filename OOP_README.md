# 🏛️ The Pillars of Object-Oriented Programming (OOP) in IANGPT

This project is built using Object-Oriented Programming (OOP) principles to ensure the code is modular, reusable, and easy to maintain. Below are the four core pillars of OOP as they are implemented in this repository.

---

## 1. 📦 Encapsulation
**"Keep it private, keep it safe."**

Encapsulation bundles data (attributes) and the methods that operate on that data into a single unit (a class). It hides the internal state from the outside world, providing a clean interface.

### 🔍 Project Example:
In `core/chat.py`, the `BaseChatSession` class encapsulates everything needed for a chat conversation.

```python
class BaseChatSession(ABC):
    def __init__(self, session_id: str = None):
        self.client = get_client()
        self.messages: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.model = MODEL_NAME
        self.session_id = session_id
```

**Why it matters:**
Instead of having global variables for messages or the AI client, they are "encapsulated" inside the session object. This allows us to have multiple independent chat sessions running at once without them interfering with each other.

📍 **Location:** [core/chat.py:L7-22](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L7-L22)

---

## 2. 🌳 Inheritance
**"Don't reinvent the wheel."**

Inheritance allows a class (child) to acquire the properties and behaviors of another class (parent). This promotes code reusability.

### 🔍 Project Example:
We use a base class for all chats, then specialized versions for different model types.

```python
# Parent Class
class BaseChatSession(ABC): ...

# Child Classes (Inherit from BaseChatSession)
class StandardChatSession(BaseChatSession): ...
class ReasoningChatSession(BaseChatSession): ...
```

**Why it matters:**
Both `StandardChatSession` and `ReasoningChatSession` automatically get the `__init__` logic and the `_generate_title_if_needed` method from the parent. We only write the code once!

📍 **Locations:**
- Parent: [core/chat.py:L7](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L7)
- Child 1: [core/chat.py:L52](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L52)
- Child 2: [core/chat.py:L94](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L94)

---

## 3. 🎭 Polymorphism
**"One interface, many forms."**

Polymorphism allows different classes to be treated as if they were the same type through a shared interface. Usually, this involves overriding methods.

### 🔍 Project Example:
Both chat session types have a `send_message` method, but they behave differently.

```python
# In StandardChatSession:
def send_message(self, content: str):
    # Standard logic for normal models

# In ReasoningChatSession:
def send_message(self, content: str):
    # Specialized logic to handle reasoning/thoughts
```

**Why it matters:**
In `app.py`, we can simply call `session.send_message(user_input)` without needing to know *which* type of session it is. The object "knows" how to handle itself.

📍 **Locations:**
- Standard: [core/chat.py:L54](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L54)
- Reasoning: [core/chat.py:L96](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L96)

---

## 💡 4. Abstraction
**"Hide the complexity, show the essentials."**

Abstraction focuses on *what* an object does rather than *how* it does it. We use Abstract Base Classes (ABC) to define a contract.

### 🔍 Project Example:
The `BaseChatSession` is an "Abstract" class. You cannot create a `BaseChatSession` directly; you must use one of its concrete implementations.

```python
@abstractmethod
def send_message(self, content: str) -> Any:
    pass
```

**Why it matters:**
It forces any new type of chat session we create in the future to implement `send_message`. It defines the "rules" of what a chat session must be able to do, while hiding the complex API calls inside the methods.

📍 **Location:** [core/chat.py:L43-49](file:///c:/code_vs/IANGPT/IANGPT/core/chat.py#L43-L49)

---

### 🚀 Quick Summary
| Pillar | Purpose | Real-World Match |
| :--- | :--- | :--- |
| **Encapsulation** | Data Security | `self.messages` inside the class |
| **Inheritance** | Reusability | `ReasoningChatSession` inheriting logic |
| **Polymorphism** | Flexibility | Multiple versions of `send_message` |
| **Abstraction** | Simplicity | `@abstractmethod` defining the contract |

Happy Coding! 💻✨
