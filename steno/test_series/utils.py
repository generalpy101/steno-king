import difflib
import math


def generate_diff_html_and_stats(original_text, typed_text, duration_seconds):
    """
    Compare original_text and typed_text on a word-by-word basis.
    Returns:
      - diff_html: a string containing HTML markup where:
           • correct words appear normally,
           • replaced/incorrect words are wrapped in <span class="incorrect">...</span>,
           • omissions (words in the original that were not typed) are wrapped in <span class="omission">...</span>.
      - stats: a dictionary with various typing statistics.

    The formulas here use the standard assumption that one word = 5 keystrokes.
    """
    # Split texts into words (you can improve this tokenizer as needed)
    orig_tokens = original_text.split()
    typed_tokens = typed_text.split()

    # Create a SequenceMatcher instance
    sm = difflib.SequenceMatcher(None, orig_tokens, typed_tokens)
    opcodes = sm.get_opcodes()

    # Prepare lists to hold the HTML segments and counters for stats.
    html_segments = []
    correct_words = 0
    incorrect_words = 0
    omissions = 0
    incorrect_characters = (
        0  # sum of characters in tokens flagged as wrong (or inserted)
    )

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            # These words match perfectly.
            segment = " ".join(orig_tokens[i1:i2])
            html_segments.append(segment)
            correct_words += i2 - i1
        elif tag == "replace":
            # Words differ.
            # We treat the user-typed segment as wrong (red) and also show the corresponding omitted original words (yellow).
            typed_segment = " ".join(typed_tokens[j1:j2])
            orig_segment = " ".join(orig_tokens[i1:i2])

            # Wrap the typed (incorrect) text:
            html_segments.append(
                f'<span class="incorrect bg-red-200 text-red-800 px-1 rounded	">{typed_segment}</span>'
            )
            # Also display the original words that were “lost”:
            html_segments.append(
                f'<span class="omission bg-yellow-200 text-yellow-800 px-1 rounded	">[{orig_segment}]</span>'
            )

            incorrect_words += j2 - j1
            omissions += i2 - i1
            incorrect_characters += sum(len(token) for token in typed_tokens[j1:j2])
        elif tag == "delete":
            # User completely omitted these words.
            orig_segment = " ".join(orig_tokens[i1:i2])
            html_segments.append(
                f'<span class="omission bg-yellow-200 text-yellow-800 px-1 rounded	">[{orig_segment}]</span>'
            )
            omissions += i2 - i1
        elif tag == "insert":
            # Extra words typed that do not appear in the original.
            typed_segment = " ".join(typed_tokens[j1:j2])
            html_segments.append(
                f'<span class="incorrect bg-red-200 text-red-800 px-1 rounded	">{typed_segment}</span>'
            )
            incorrect_words += j2 - j1
            incorrect_characters += sum(len(token) for token in typed_tokens[j1:j2])

    diff_html = " ".join(html_segments)

    # Basic stats
    total_words_in_passage = len(orig_tokens)
    total_typed_words = len(typed_tokens)
    keystrokes = len(typed_text)  # you might choose to count only non-space characters

    # Standard formulas: one “word” = 5 characters.
    minutes = duration_seconds / 60.0
    gross_wpm = (keystrokes / 5) / minutes if minutes > 0 else 0

    # For net WPM, subtract error penalty.
    # Here we subtract one “word” per incorrect word.
    net_wpm = gross_wpm - (incorrect_words / minutes) if minutes > 0 else 0
    if net_wpm < 0:
        net_wpm = 0

    # Accuracy can be computed as ratio of correct words to total typed words.
    speed_accuracy = (
        (correct_words / total_typed_words * 100) if total_typed_words > 0 else 0
    )

    # Keystrokes per hour (KDPH)
    gross_kdph = keystrokes * (3600 / duration_seconds) if duration_seconds > 0 else 0
    # Estimate net KDPH by removing incorrect keystrokes
    net_keystrokes = keystrokes - incorrect_characters
    net_kdph = net_keystrokes * (3600 / duration_seconds) if duration_seconds > 0 else 0

    # Error percentage based on the typed word count.
    error_percentage = (
        (incorrect_words / total_typed_words * 100) if total_typed_words > 0 else 0
    )

    stats = {
        "total_words_in_passage": total_words_in_passage,
        "total_typed_words": total_typed_words,
        "correct_words": correct_words,
        "incorrect_words": incorrect_words,
        "omissions": omissions,
        "keystrokes": keystrokes,
        "typing_duration_seconds": duration_seconds,
        "gross_typing_speed_wpm": math.floor(gross_wpm),
        "net_typing_speed_wpm": math.floor(net_wpm),
        "speed_accuracy_percent": round(speed_accuracy, 1),
        "gross_typing_speed_kdph": math.floor(gross_kdph),
        "net_typing_speed_kdph": math.floor(net_kdph),
        "error_percentage": round(error_percentage, 1),
    }

    return diff_html, stats


# ----- Example usage -----

if __name__ == "__main__":
    # Sample original and user typed texts.
    original = (
        "Geography is the study of the Earth's physical features, climate, and the relationship between the environment "
        "and human activities. [Text continues]"
    )
    # The user mistakenly merged some words and omitted others.
    typed = (
        "Geography is the syudyof the Earth'sphysical features, climate, andtat relationship between the environment "
        "and human activities."
    )

    # For example, assume the user took 600 seconds (10 minutes) for the test.
    duration_sec = 600

    diff_html, stats = generate_diff_html_and_stats(original, typed, duration_sec)

    print("=== Diff Markup ===")
    print(diff_html)
    print("\n=== Statistics ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
