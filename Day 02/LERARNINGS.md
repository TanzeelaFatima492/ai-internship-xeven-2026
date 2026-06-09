# LEARNINGS.md - Day 02

## Date

Day 02 - Python Basics: Variables, Data Types, Memory & Core Concepts

## Topics Covered

- Python overview
- Variables and dynamic typing
- Python data types
- Mutable vs immutable objects
- Memory management
- Input and output
- Type conversion
- Error handling
- Basic calculator program

## Key Learnings

### 1. Python is Dynamically Typed

Python does not require explicit variable type declarations. A variable can store different data types during program execution.

Example:

```python
x = 10
x = "Hello"
```

### 2. Everything in Python is an Object

Numbers, strings, lists, and functions are all objects with their own properties and methods.

### 3. Python Data Types

The primary built-in data types studied were:

- Integer (`int`)
- Float (`float`)
- Boolean (`bool`)
- String (`str`)
- List (`list`)

Each data type serves different purposes depending on the application.

### 4. Mutable vs Immutable Objects

**Immutable objects:**

- int
- float
- bool
- str
- tuple

Their values cannot be modified after creation.

**Mutable objects:**

- list
- dictionary
- set

Their contents can be changed without creating a new object.

### 5. Memory Management

Python automatically manages memory using:

- Reference counting
- Garbage collection

The `id()` function can be used to inspect an object's identity in memory.

### 6. Dynamic Typing

Variables store references to objects rather than fixed data types, allowing reassignment to different object types.

### 7. Input and Output

The `input()` function collects user input as a string, while `print()` displays output.

Example:

```python
name = input("Enter your name: ")
print(name)
```

### 8. Type Conversion

Data can be converted between types using built-in functions.

Common conversions:

- `int()`
- `float()`
- `str()`
- `bool()`

Type conversion is necessary when performing arithmetic on user input.

### 9. Error Handling

Python uses `try-except` blocks to handle runtime errors gracefully.

Common exceptions studied:

- `ValueError`
- `ZeroDivisionError`

This prevents programs from crashing unexpectedly.

### 10. Calculator Implementation

A simple calculator was developed that:

- Accepts two user inputs.
- Performs addition, subtraction, multiplication, and division.
- Handles invalid input.
- Prevents division by zero errors.

## Research Insights

### Why Python is Popular

- Easy to learn and read.
- Cross-platform compatibility.
- Large standard library.
- Strong community support.
- Widely used in AI, web development, automation, and data science.

### Why Error Handling Matters

- Improves program reliability.
- Enhances user experience.
- Makes applications more robust and maintainable.

### Why Understanding Mutability is Important

Knowing whether an object is mutable or immutable helps avoid unintended side effects and write more efficient code.

# Practical Skills Gained

After Day 02, I can:

- Declare and use variables.
- Work with Python data types.
- Perform type conversions.
- Take user input and display output.
- Understand object identity and memory basics.
- Differentiate between mutable and immutable objects.
- Implement basic error handling.
- Build a simple interactive calculator.

## Reflection

Day 02 strengthened my understanding of Python fundamentals. The concepts of dynamic typing, object identity, mutability, and exception handling provided insight into how Python manages data and executes programs. Building a calculator combined these concepts into a practical application and reinforced the importance of writing reliable, user-friendly code.
