## Python Collections

### Python has three core collection types beginners must know: lists, tuples, and sets.

**Lists** use square brackets [ ] and are ordered, mutable sequences that allow duplicates; you can add, remove, or modify items freely. Tuples use parentheses ( ) and are ordered but immutable once created their contents cannot change, making them faster and safer for fixed data like coordinates; they also support packing and unpacking (e.g., name, age = ("Ali", 25)).

**Sets** use curly braces { } and store unordered, unique elements; duplicates are automatically removed. Sets are implemented with hashing much faster than scanning a list. Choose structures by need: use lists for ordered, changeable collections.

**tuples** when data must remain constant; sets when uniqueness or fast membership tests matter. Practical exercises include a visitor tracker and email validator: tuples for fixed records, sets to prevent duplicate registrations, and lists for ordered sequences.

Common beginner errors encountered were indentation mistakes, wrong filenames in Git, KeyboardInterrupt from manual stops, and misunderstanding immutability tuple object does not support item assignment . Understanding these distinctions leads to cleaner and more efficient Python code.
