
import random
import pandas as pd

# 📊 DATASET (20 SAMPLES)
samples = [
    "I love this product, it's amazing!",
    "This is the worst experience ever.",
    "It's okay, not bad but not great.",
    "Absolutely fantastic service!",
    "I hate it so much.",
    "Pretty good overall.",
    "Not what I expected.",
    "Excellent quality!",
    "Very disappointing.",
    "I am happy with this.",
    "Totally useless item.",
    "Works fine for me.",
    "Worst purchase ever.",
    "I really like it.",
    "It is average.",
    "Superb experience!",
    "Not good not bad.",
    "I enjoyed using this.",
    "Terrible quality.",
    "Satisfied with product."
]

labels = [
    "Positive","Negative","Neutral","Positive","Negative",
    "Positive","Negative","Positive","Negative","Positive",
    "Negative","Positive","Negative","Positive","Neutral",
    "Positive","Neutral","Positive","Negative","Positive"
]

# 🧠 SIMPLE MOCK AI MODEL
def mock_model(text):
    text = text.lower()

    if "love" in text or "excellent" in text or "amazing" in text or "fantastic" in text:
        return "Positive"
    elif "hate" in text or "worst" in text or "terrible" in text or "useless" in text:
        return "Negative"
    else:
        return random.choice(["Positive", "Negative", "Neutral"])


#  ZERO-SHOT PROMPTING
def zero_shot():
    predictions = []
    for text in samples:
        prompt = "Classify sentiment as Positive, Negative, or Neutral: " + text
        predictions.append(mock_model(text))
    return predictions


#  FEW-SHOT PROMPTING
def few_shot():
    predictions = []

    examples = """
    Text: I love this movie → Positive
    Text: I hate this movie → Negative
    Text: It is okay → Neutral
    """

    for text in samples:
        prompt = examples + "\nText: " + text
        predictions.append(mock_model(text))
    return predictions

# CHAIN-OF-THOUGHT (COT)
def chain_of_thought():
    predictions = []

    for text in samples:
        prompt = f"""
        Step 1: Identify emotion words
        Step 2: Understand context
        Step 3: Decide sentiment

        Text: {text}
        """

        # improved logic simulation
        if any(word in text.lower() for word in ["love","amazing","excellent","fantastic","happy"]):
            predictions.append("Positive")
        elif any(word in text.lower() for word in ["hate","worst","terrible","useless"]):
            predictions.append("Negative")
        else:
            predictions.append("Neutral")

    return predictions

# 📏 ACCURACY FUNCTION
def accuracy(preds, labels):
    correct = sum([p == l for p, l in zip(preds, labels)])
    return correct / len(labels)

# 🚀 RUN ALL METHODS
zero_preds = zero_shot()
few_preds = few_shot()
cot_preds = chain_of_thought()

#  RESULTS TABLE
results = pd.DataFrame({
    "Technique": ["Zero-shot", "Few-shot", "Chain-of-Thought"],
    "Accuracy (%)": [
        round(accuracy(zero_preds, labels)*100, 2),
        round(accuracy(few_preds, labels)*100, 2),
        round(accuracy(cot_preds, labels)*100, 2)
    ],
    "Speed": ["Fast", "Medium", "Slow"],
    "Cost": ["Low", "Medium", "High"],
    "Best Use Case": [
        "Simple classification",
        "Pattern learning",
        "Complex reasoning tasks"
    ]
})

print("\nPROMPTING TECHNIQUE COMPARISON RESULTS\n")
print(results)