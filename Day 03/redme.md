
# Python Conditionals — Task 1 & Task 2

**Author:** Tanzeela  
**Topic:** Conditional Statements, Boolean Logic, Error Handling  
**Language:** Python 3

---

## Project Overview

Two Python programs demonstrating conditional logic with proper input validation and error handling.

| File | Description |
|---|---|
| `task1_age_verification.py` | Age-based category classifier |
| `task2_grade_calculator.py` | Numeric grade to letter grade converter |
| `notebook.ipynb` | Jupyter notebook with flowcharts and all code |

---

## Task 1 — Age Verification System

Prompts user for name and age, then classifies into one of four categories with a personalized message.

### Categories

| Age Range | Category | Message |
|---|---|---|
| 0 – 12 | Child | "Enjoy your childhood..." |
| 13 – 17 | Teenager | "Many opportunities ahead..." |
| 18 – 64 | Adult | "You are in your prime..." |
| 65+ | Senior | "Your wisdom is valuable..." |

### How to Run

```bash
python task1_age_verification.py
```

### Sample Output

```
Enter your name : John
Enter your age  : 15

Hello John! As a teenager, you have many opportunities ahead.
```

### Error Handling

| Invalid Input | Response |
|---|---|
| Empty name | "Name cannot be empty" |
| Negative age | "Age cannot be negative" |
| Age > 150 | "That age is unrealistic" |
| Text like "abc" | "Please enter a whole number" |

---

## Task 2 — Grade Calculator

Accepts a numeric grade (0–100) and returns a letter grade with an encouraging message.

### Grade Scale

| Range | Letter | Message |
|---|---|---|
| 90 – 100 | A | Excellent work! |
| 80 – 89 | B | Good job! |
| 70 – 79 | C | Keep it up! |
| 60 – 69 | D | You can do better! |
| 0 – 59 | F | Don't give up! |

### How to Run

```bash
python task2_grade_calculator.py
```

### Sample Output

```
Enter student name         : Sara
Enter numeric grade (0-100): 95

==================================================
  Student : Sara
  Score   : 95.0 / 100
  Grade   : A
  Result  : Excellent work!
  Note    : Outstanding — you mastered the material.
==================================================
```

### Error Handling

| Invalid Input | Response |
|---|---|
| Empty name | "Name cannot be empty" |
| Grade > 100 | "Grade cannot exceed 100" |
| Grade < 0 | "Grade cannot be below 0" |
| Text like "abc" | "Please enter a numeric grade" |

---

## Concepts Used

- `if / elif / else` — conditional flow control
- `try / except ValueError` — error handling for invalid input
- `f-strings` — personalized output messages
- `float()` and `int()` — type conversion from string input
- `str.strip()` — empty input validation
- Efficient `elif` chain — no unnecessary nesting

---

## Requirements

- Python 3.x
- No external libraries needed

---

## How to Run Both Programs

```bash
# Clone or download the files, then:

python task1_age_verification.py
python task2_grade_calculator.py

# For Jupyter notebook:
jupyter notebook notebook.ipynb
```
