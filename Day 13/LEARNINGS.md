
Functions encapsulate behavior with def; they accept parameters and return values (or None by default). Positional and keyword arguments control calling flexibility; default parameters provide fallbacks. Use *args and **kwargs for flexible argument capture and unpacking. Scope follows LEGB (Local, Enclosing, Global, Built-in); local variables are transient. Design functions with single responsibility, descriptive snake_case names, and docstrings to keep code maintainable and testable.

Comprehensions & Lambdas
List and dictionary comprehensions concisely build collections: [expr for x in iterable if cond] and {k:v for ...}. They are fast and readable for simple transforms but avoid over-nesting. Lambda expressions are compact anonymous functions useful for small callbacks (map/filter/sorted). For huge datasets, prefer generator expressions or streaming to save memory.
