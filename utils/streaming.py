import time

def stream_print(text, delay=0.03):
    """Prints text to the terminal one character at a time, like typing."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Newline at the end

def stream_print_words(text, delay=0.15):
    """Prints text to the terminal one word at a time, like typing."""
    for word in text.split():
        print(word + " ", end='', flush=True)
        time.sleep(delay)
    print()
