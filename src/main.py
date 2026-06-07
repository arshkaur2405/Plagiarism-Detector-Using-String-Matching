
"""
main.py: Plagiarism Detector using String Matching Algorithms (Naive, KMP, Rabin-Karp).
"""
import re
import sys
import argparse

# Function to read file content
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

# Function to clean text: lowercase, remove punctuation, normalize spaces
def clean_text(text):
    """
    Convert text to lowercase, remove non-alphanumeric characters,
    and collapse multiple spaces.
    """
    text = text.lower()
    # Replace non-alphanumeric characters with spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Collapse multiple spaces into a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to split text into sentences (simple split on .,!,?)
def split_sentences(text):
    """
    Split text into sentences based on punctuation.
    """
    sentences = re.split(r'[.!?]+', text)
    # Strip whitespace and remove empty strings
    return [s.strip() for s in sentences if s.strip()]

# Naive string search: find occurrences of a pattern in text
def naive_search(text, pattern):
    """
    Return a list of start indices where pattern matches text (Naive search).
    """
    matches = []
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            matches.append(i)
    return matches

# KMP (Knuth-Morris-Pratt) string matching implementation
def compute_lps(pattern):
    """
    Compute the LPS (longest proper prefix which is also suffix) array for KMP.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix suffix
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
                # No increment of i here
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """
    Return a list of start indices where pattern matches text (KMP search).
    """
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches = []
    i = j = 0  # i-> index for text, j-> index for pattern
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]  # continue searching for next match
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

# Rabin-Karp string matching implementation
def rabin_karp_search(text, pattern, prime=101):
    """
    Return a list of start indices where pattern matches text (Rabin-Karp search).
    Uses a rolling hash for pattern matching.
    """
    matches = []
    n, m = len(text), len(pattern)
    if m > n:
        return matches

    d = 256  # number of characters in input alphabet
    h = 1
    p_hash = 0  # hash for pattern
    t_hash = 0  # hash for text

    # The value of h would be "pow(d, m-1) % prime"
    for i in range(m - 1):
        h = (h * d) % prime

    # Calculate initial hash values for pattern and first text window
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % prime
        t_hash = (d * t_hash + ord(text[i])) % prime

    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # If hashes match, check characters one by one to avoid collision
        if p_hash == t_hash:
            if text[i:i+m] == pattern:
                matches.append(i)
        # Compute hash for next window of text
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime
    return matches

# Compute plagiarism percentage and collect matched phrases
def analyze_similarity(original_text, submitted_text, algorithm):
    """
    Analyze similarity between original and submitted text using a specific algorithm.
    Returns plagiarism percentage and list of matched phrases.
    """
    # Clean original text for uniform comparison
    original_clean = clean_text(original_text)
    # Split submitted document into sentences using punctuation
    submitted_sents = split_sentences(submitted_text)
    total_length = len(clean_text(submitted_text))
    matched_length = 0
    matched_phrases = []

    # Select the search function based on algorithm
    if algorithm == 'naive':
        search_func = naive_search
    elif algorithm == 'kmp':
        search_func = kmp_search
    elif algorithm == 'rabin':
        search_func = rabin_karp_search
    else:
        search_func = None

    matched_set = set()  # to avoid double-counting

    for sent in submitted_sents:
        # Clean each sentence separately
        sent_clean = clean_text(sent)
        if not sent_clean or len(sent_clean) < 5:
            continue  # skip short or empty
        indices = search_func(original_clean, sent_clean)
        if indices:
            if sent_clean not in matched_set:
                matched_set.add(sent_clean)
                matched_phrases.append(sent_clean)
                matched_length += len(sent_clean)

    # Calculate percentage of submitted text that is plagiarized
    plagiarism_percent = (matched_length / total_length) * 100 if total_length > 0 else 0.0
    return plagiarism_percent, matched_phrases

# Generate a formatted report string
def generate_report(algorithm, plagiarism_percent, matched_phrases):
    """
    Create a report string showing the chosen algorithm, plagiarism percentage,
    and matched phrases.
    """
    report_lines = []
    report_lines.append(f"Algorithm: {algorithm.upper()}\n")
    report_lines.append(f"Plagiarism Percentage: {plagiarism_percent:.2f}%\n")
    report_lines.append("Matched Phrases:\n")
    if matched_phrases:
        for phrase in matched_phrases:
            report_lines.append(f" - {phrase}\n")
    else:
        report_lines.append(" - None\n")
    report_lines.append("\n")
    return "".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description="Plagiarism Detector using String Matching Algorithms")
    parser.add_argument('-o', '--original', type=str, required=True,
                        help="Original document file (text)")
    parser.add_argument('-s', '--submitted', type=str, required=True,
                        help="Submitted document file to check")
    parser.add_argument('-a', '--algorithm', type=str, choices=['naive', 'kmp', 'rabin', 'all'],
                        default='all', help="Algorithm to use: naive, kmp, rabin, or all (compare)")
    args = parser.parse_args()

    original_text = read_file(args.original)
    submitted_text = read_file(args.submitted)

    # Run the chosen algorithm(s) and display results
    if args.algorithm == 'all':
        for alg in ['naive', 'kmp', 'rabin']:
            percent, phrases = analyze_similarity(original_text, submitted_text, alg)
            report = generate_report(alg, percent, phrases)
            print(report)
    else:
        percent, phrases = analyze_similarity(original_text, submitted_text, args.algorithm)
        report = generate_report(args.algorithm, percent, phrases)
        print(report)

if __name__ == "__main__":
    main()
