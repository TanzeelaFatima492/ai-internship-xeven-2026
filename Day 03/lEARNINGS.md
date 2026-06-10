
# Learnings — Day 03 Practice Session

**Author:** Tanzeela  
**Date:** June 2026  
**Tasks:** Age Verification System & Grade Calculator

---

## What I Learned Today

### 1. f-strings Syntax
The biggest mistake I made was writing `print(f("Hello {name}"))` instead of
`print(f"Hello {name}")`. The `f` is not a function — it is a prefix before
the string. Without it, `{name}` prints literally instead of the variable value.

### 2. Input Validation Order Matters
For age verification, I learned that negative age must be checked **before**
category classification. If `age < 0` check comes after `elif age < 13`, then
`-8` incorrectly gets classified as a Child.

### 3. int() vs float()
Using `int()` on grade input caused a crash when user typed `9.0`. The fix is
to use `float()` first — it accepts both `9` and `9.0` without error.

### 4. try-except Saves the Program
Without `try-except`, typing `hjuh` as a grade crashes the entire program.
Wrapping input in `try-except ValueError` handles invalid input gracefully.

### 5. Git Commands
Learned that typos in Git matter — `got commit` and `git puh` both failed.
Also, `cd Day 03` needs quotes in PowerShell: `cd "Day 03"`.

---

> *"Every bug I fixed today taught me more than any correct code could."*