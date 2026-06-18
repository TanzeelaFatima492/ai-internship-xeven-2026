# LEARNINGS.md

This project focused on understanding and applying core Prompt Engineering techniques used in modern AI systems. I learned how different prompting strategies directly affect the accuracy, structure, and reasoning ability of AI models.

First, I explored **Zero-shot prompting**, where only instructions are given without examples. It is fast and simple but less accurate for complex tasks. Then I studied **Few-shot prompting**, where 2–5 examples are provided to guide the model. This significantly improves accuracy by helping the model learn patterns.

Next, I learned **Chain-of-Thought (CoT) prompting**, which encourages step-by-step reasoning. This is highly effective for mathematical, logical, and multi-step problems, though it is slower and more computationally expensive.

I also learned about **System messages**, which define the AI’s role, tone, and constraints before any user input. Additionally, I studied **Prompt patterns**, which include persona, instruction, context, format, examples, and constraints to structure effective prompts.

I built a **Prompt Template Library** using JSON structure to reuse prompts for tasks like summarization, extraction, generation, and analysis.

Finally, I explored **Advanced Output Control**, including strict JSON formatting, markdown table generation, and code generation with rules and constraints. I also tested robustness using edge cases.

Overall, I learned how structured prompting improves AI reliability and output quality.