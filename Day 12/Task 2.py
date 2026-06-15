import string
import re

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def count_words(text):
    return len(text.split())

def extract_emails(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)

def title_case(text):
    return text.title()

def process_text(text, remove_punct=True, to_title=False):
    if remove_punct:
        text = remove_punctuation(text)

    if to_title:
        text = title_case(text)

    return text


def text_stats(text):
    cleaned = remove_punctuation(text)
    words = cleaned.split()

    word_count = len(words)
    char_count = len(text)
    unique_words = len(set(words))

    return word_count, char_count, unique_words

if __name__ == "__main__":

    sample_text = """
    Hello world! This is Python programming.
    Contact: test@gmail.com or admin@example.com.
    Python is powerful, Python is easy.
    """

    print("Original Text:\n", sample_text)

    print("\n--- Basic Functions ---")
    print("Word Count:", count_words(sample_text))
    print("Emails Found:", extract_emails(sample_text))

    print("\n--- Processed Text ---")
    print(process_text(sample_text, remove_punct=True, to_title=True))

    print("\n--- Text Statistics ---")
    wc, cc, uw = text_stats(sample_text)
    print("Words:", wc)
    print("Characters:", cc)
    print("Unique Words:", uw)