A function is a reusable block of code that performs a specific task, defined with the def keyword. It can accept inputs called parameters and produce outputs via return; if no return is provided, Python returns None implicitly. Arguments are the actual values passed at call time. Positional arguments match parameters by order, while keyword arguments match by name, improving clarity. Default parameters supply fallback values when callers omit arguments. Argument unpacking with *args (collects extra positional arguments into a tuple) and **kwargs (collects extra keyword arguments into a dict) makes functions flexible.

Scope determines where a name is visible; follow the LEGB rule (Local, Enclosing, Global, Built-in). Local variables exist only during the function call and are garbage-collected afterward, keeping the global namespace clean. Use the global keyword only when you intentionally need to modify module-level variables.

Good function design follows the Single Responsibility Principle: one function, one clear task. Favor descriptive snake_case names and include docstrings (PEP 257) that explain purpose, parameters, return values, and side effects. Keep functions short, avoid hidden global state, and write tests for edge cases. Together, these practices produce modular, readable, and maintainable code suitable for production.


