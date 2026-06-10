# Learnings from Python Operators, Errors, and New Terminology

During this task, I strengthened my understanding of Python operators, operator precedence, type conversion, and how real-world errors occur during program execution. I learned that arithmetic operators such as +, -, *, /, //, %, and ** are used for mathematical operations, but each behaves differently. For example, / always returns a float, while // “chops off” the decimal part without rounding. This helped me understand how Python handles numbers internally.

I also learned comparison operators like ==, !=, >, <, >=, and <=, which are essential for decision-making in conditions such as age checks and login validation. Logical operators (and, or, not) allow combining multiple conditions and are very useful in form validation systems. I now understand that input values are always strings, so type conversion using int(), float(), str(), and bool() is necessary before performing calculations.

One of the most important learnings came from my errors. I faced ValueError when trying to convert “5.0” using int(), which taught me that float values cannot directly convert to integers in string form. I also learned about ZeroDivisionError when dividing by zero and how to prevent it using validation. Another error was invalid operation input, which showed the importance of input checking.

I also learned new terminology like “chops off,” meaning removing decimal parts without rounding, and short-circuit evaluation in logical operators. Operator precedence helped me understand the order in which Python executes expressions, similar to BODMAS rules.

Overall, these experiences improved my debugging skills, logical thinking, and understanding of how real-world Python applications handle errors and user input safely.