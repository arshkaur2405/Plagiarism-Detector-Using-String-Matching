# app.py


import streamlit as st
import re
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Plagiarism Detector",
    page_icon="📄",
    layout="wide"
)

# =====================================================
# TEXT PREPROCESSING
# =====================================================

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s.]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text):
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


# =====================================================
# NAIVE STRING MATCHING
# =====================================================

def naive_search(text, pattern):

    n = len(text)
    m = len(pattern)

    if m == 0:
        return False

    for i in range(n - m + 1):

        j = 0

        while j < m and text[i + j] == pattern[j]:
            j += 1

        if j == m:
            return True

    return False


# =====================================================
# KMP ALGORITHM
# =====================================================

def compute_lps(pattern):

    lps = [0] * len(pattern)

    length = 0
    i = 1

    while i < len(pattern):

        if pattern[i] == pattern[length]:

            length += 1
            lps[i] = length
            i += 1

        else:

            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):

    if len(pattern) == 0:
        return False

    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    i = 0
    j = 0

    while i < n:

        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            return True

        elif i < n and text[i] != pattern[j]:

            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False


# =====================================================
# RABIN-KARP ALGORITHM
# =====================================================

def rabin_karp(text, pattern):

    d = 256
    q = 101

    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return False

    h = 1

    for _ in range(m - 1):
        h = (h * d) % q

    pattern_hash = 0
    text_hash = 0

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q

    for i in range(n - m + 1):

        if pattern_hash == text_hash:

            if text[i:i + m] == pattern:
                return True

        if i < n - m:

            text_hash = (
                d * (text_hash - ord(text[i]) * h)
                + ord(text[i + m])
            ) % q

            if text_hash < 0:
                text_hash += q

    return False


# =====================================================
# SIMILARITY CALCULATION
# =====================================================

def calculate_similarity(original, submitted, algorithm):

    original_sentences = split_sentences(original)

    matched_sentences = []

    for sentence in original_sentences:

        if len(sentence) < 5:
            continue

        found = False

        if algorithm == "Naive String Matching":
            found = naive_search(submitted, sentence)

        elif algorithm == "KMP Algorithm":
            found = kmp_search(submitted, sentence)

        elif algorithm == "Rabin-Karp Algorithm":
            found = rabin_karp(submitted, sentence)

        if found:
            matched_sentences.append(sentence)

    total_sentences = len(original_sentences)

    plagiarism_percentage = (
        len(matched_sentences) / total_sentences * 100
    ) if total_sentences > 0 else 0

    return plagiarism_percentage, matched_sentences


# =====================================================
# REPORT GENERATION
# =====================================================

def generate_report(
        percentage,
        matched_sentences,
        total_sentences,
        algorithm):

    report = []
    report.append("PLAGIARISM DETECTION REPORT")
    report.append("=" * 50)
    report.append(
        f"Generated On: {datetime.now()}"
    )
    report.append(
        f"Algorithm Used: {algorithm}"
    )
    report.append("")

    report.append(
        f"Total Sentences: {total_sentences}"
    )
    report.append(
        f"Matched Sentences: {len(matched_sentences)}"
    )
    report.append(
        f"Plagiarism Percentage: {percentage:.2f}%"
    )

    report.append("")
    report.append("MATCHED CONTENT")
    report.append("-" * 50)

    if matched_sentences:

        for i, sentence in enumerate(
                matched_sentences,
                start=1):
            report.append(
                f"{i}. {sentence}"
            )

    else:
        report.append(
            "No matching content found."
        )

    return "\n".join(report)


# =====================================================
# HEADER
# =====================================================

st.title("📄 Plagiarism Detector")
st.subheader(
    "Using Naive, KMP & Rabin-Karp Algorithms"
)

st.markdown("---")

# =====================================================
# INPUT MODE
# =====================================================

input_mode = st.radio(
    "Select Input Method",
    [
        "Upload Files",
        "Enter Text Manually"
    ]
)

original_text = ""
submitted_text = ""

# =====================================================
# FILE UPLOAD
# =====================================================

if input_mode == "Upload Files":

    col1, col2 = st.columns(2)

    with col1:

        original_file = st.file_uploader(
            "Upload Original Document",
            type=["txt"]
        )

    with col2:

        submitted_file = st.file_uploader(
            "Upload Submitted Document",
            type=["txt"]
        )

    if original_file:
        original_text = (
            original_file.read()
            .decode("utf-8")
        )

    if submitted_file:
        submitted_text = (
            submitted_file.read()
            .decode("utf-8")
        )

# =====================================================
# MANUAL TEXT INPUT
# =====================================================

else:

    col1, col2 = st.columns(2)

    with col1:

        original_text = st.text_area(
            "Original Document",
            height=300,
            placeholder="Paste original content here..."
        )

    with col2:

        submitted_text = st.text_area(
            "Submitted Document",
            height=300,
            placeholder="Paste submitted content here..."
        )

# =====================================================
# ALGORITHM SELECTION
# =====================================================

algorithm = st.selectbox(
    "Choose String Matching Algorithm",
    [
        "Naive String Matching",
        "KMP Algorithm",
        "Rabin-Karp Algorithm"
    ]
)

# =====================================================
# DETECT BUTTON
# =====================================================

if st.button("🔍 Detect Plagiarism"):

    if not original_text.strip() or not submitted_text.strip():

        st.error(
            "Please provide both documents."
        )

    else:

        processed_original = preprocess_text(
            original_text
        )

        processed_submitted = preprocess_text(
            submitted_text
        )

        percentage, matched = calculate_similarity(
            processed_original,
            processed_submitted,
            algorithm
        )

        total_sentences = len(
            split_sentences(
                processed_original
            )
        )

        report = generate_report(
            percentage,
            matched,
            total_sentences,
            algorithm
        )

        st.success(
            "Analysis Completed Successfully!"
        )

        st.metric(
            "Plagiarism Percentage",
            f"{percentage:.2f}%"
        )

        st.info(
            f"Algorithm Used: {algorithm}"
        )

        st.markdown("---")

        st.subheader(
            "Matched Sentences"
        )

        if matched:

            for i, sentence in enumerate(
                    matched,
                    start=1):

                st.success(
                    f"{i}. {sentence}"
                )

        else:

            st.warning(
                "No matching content detected."
            )

        st.markdown("---")

        st.subheader(
            "Document Comparison"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.text_area(
                "Processed Original",
                processed_original,
                height=250
            )

        with col2:

            st.text_area(
                "Processed Submitted",
                processed_submitted,
                height=250
            )

        st.markdown("---")

        st.subheader(
            "Algorithm Complexity"
        )

        if algorithm == "Naive String Matching":

            st.code("""
Time Complexity : O(n × m)
Space Complexity: O(1)
            """)

        elif algorithm == "KMP Algorithm":

            st.code("""
Time Complexity : O(n + m)
Space Complexity: O(m)
            """)

        else:

            st.code("""
Average Time Complexity : O(n + m)
Worst Case Complexity   : O(n × m)
Space Complexity        : O(1)
            """)

        st.markdown("---")

        st.subheader(
            "Generated Report"
        )

        st.code(report)

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="plagiarism_report.txt",
            mime="text/plain"
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "DSA Project | Plagiarism Detector Using String Matching Algorithms"
)

