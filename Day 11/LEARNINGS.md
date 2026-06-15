## 1. For Loops: Sequence Iteration

A `for` loop in Python acts as an iterator that steps through items in any sequence (like a list, tuple, string, or dictionary) in the order they appear.

### Essential Iteration Tools

Python provides built-in functions to make sequence iteration cleaner and more powerful:

- **`range(start, stop, step)`:** Generates a sequence of numbers. It is highly memory-efficient because it generates numbers on the fly rather than creating a massive list in memory.
- **`enumerate()`:** Yields pairs of `(index, item)` simultaneously. This eliminates the need to manually manage a counter variable.
- **`zip()`:** Pairs elements from multiple iterables parallelly. It stops as soon as the shortest iterable is exhausted.

## 2. While Loops: Condition-Based Iteration

A `while` loop repeatedly executes a block of code as long as a specified boolean condition remains `True`.

### The Risk of Infinite Loops

If the loop's condition never becomes `False`, the program enters an **infinite loop**, consuming CPU resources until it crashes or is forcefully terminated. You must always ensure the loop body updates a variable that eventually breaks the condition.

## 3. Loop Control: Break, Continue, and Else

Python gives you granular control over execution flow mid-loop through specific keyword directives.

### Control Statements

- **`break`:** Terminates the loop entirely and jumps to the next statement outside the loop.
- **`continue`:** Skips the rest of the current iteration's code block and jumps straight to the evaluation of the next iteration.
- **`else` (with loops):** A unique Python feature. The `else` block executes **only if the loop finished naturally** (i.e., it ran to completion without encountering a `break` statement). This is incredibly helpful for search operations.

## 4. Nested Loops: 2D Processing & Complexity

A nested loop is a loop inside another loop. The inner loop executes all of its iterations for _every single iteration_ of the outer loop.

### Matrix Operations and 2D Data

Nested loops are the foundational way to process grids, coordinates, images, or 2D matrices.

### Time Complexity: $O(n^2)$

When analyzing performance, nested loops can quickly become expensive:

- If the outer loop runs $n$ times and the inner loop also runs $n$ times, the total operations scale quadratically: $n \times n = n^2$.
- In Big O notation, this is expressed as **$O(n^2)$ time complexity**.
- **Performance Impact:** If $n = 100$, the code runs 10,000 times. If $n = 100,000$, it scales to 10 billion operations, causing severe lags. As an AI engineer, optimizing away from nested loops using vectorized operations (like NumPy or PyTorch tensors) is a critical optimization technique.

## Decision Matrix: For vs. While Loops

| Scenario             | Use a `for` Loop                                        | Use a `while` Loop                                             |
| -------------------- | ------------------------------------------------------- | -------------------------------------------------------------- |
| **Iteration Count**  | Known beforehand or bound to a sequence.                | Unknown; dependent on an event or external flag.               |
| **Primary Use Case** | Stepping through arrays, indices, or database records.  | Listening for user inputs, polling APIs, games.                |
| **Risk Factor**      | Low risk (guaranteed to terminate via sequence length). | High risk of infinite loops if state variables fail to update. |
