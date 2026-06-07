# 📄 Plagiarism Detector Using String Matching Algorithms

## 🚀 Project Overview

The **Plagiarism Detector Using String Matching Algorithms** is a Data Structures and Algorithms (DSA) project that detects similarities between text documents using classical pattern matching techniques.

The system compares an **Original Document** and a **Submitted Document**, identifies copied content, calculates the plagiarism percentage, and generates a detailed report.

The project demonstrates how string matching algorithms can be applied to solve real-world problems such as plagiarism detection, content verification, and text similarity analysis.

---

# 🎯 Problem Statement

Plagiarism is a major concern in educational institutions, publishing platforms, online learning systems, and content management platforms.

Manually checking documents for copied content is time-consuming and inefficient.

This project automates plagiarism detection using efficient string matching algorithms.

---

# ✨ Features

* Upload Original and Submitted Documents
* Manual Text Input
* Automatic Loading of Sample Documents
* Text Preprocessing
* Sentence Tokenization
* Naive String Matching Algorithm
* Knuth-Morris-Pratt (KMP) Algorithm
* Rabin-Karp Algorithm
* Similarity Calculation
* Plagiarism Percentage Detection
* Matched Sentence Identification
* Downloadable Report Generation
* Interactive Streamlit Dashboard

---

# 🏗️ Project Architecture

```text
Original Document
        │
        ▼
Text Preprocessing
        │
        ▼
Sentence Splitting
        │
        ▼
String Matching Algorithms
(Naive / KMP / Rabin-Karp)
        │
        ▼
Similarity Calculation
        │
        ▼
Matched Content Detection
        │
        ▼
Plagiarism Percentage
        │
        ▼
Report Generation
```

---

# 🧠 DSA Concepts Used

## String Matching

Used to compare text patterns between documents.

## Pattern Searching

Detects copied content efficiently.

## Hashing

Used in Rabin-Karp Algorithm.

## Prefix Function (LPS Array)

Used in KMP Algorithm.

## Arrays

Used for storing prefix values and sentences.

## File Handling

Reading text documents.

## Text Processing

Cleaning and tokenizing documents.

---

# ⚙️ Algorithms Implemented

## 1. Naive String Matching

Compares the pattern against every possible position in the text.

### Time Complexity

```text
O(n × m)
```

### Space Complexity

```text
O(1)
```

---

## 2. KMP Algorithm

Uses an LPS (Longest Prefix Suffix) array to avoid unnecessary comparisons.

### Time Complexity

```text
O(n + m)
```

### Space Complexity

```text
O(m)
```

---

## 3. Rabin-Karp Algorithm

Uses hashing and rolling hash techniques for pattern matching.

### Average Time Complexity

```text
O(n + m)
```

### Worst Case

```text
O(n × m)
```

### Space Complexity

```text
O(1)
```

---

# 💻 Tech Stack

* Python
* Streamlit
* Regular Expressions (re)
* File Handling
* Git
* GitHub

---

# 📂 Folder Structure

```text
Plagiarism-Detector-Using-String-Matching/
│
├── documents/
│   ├── original.txt
│   └── submitted.txt
│
├── reports/
│
├── outputs/
│
├── images/
│
├── src/
     |--app.py
     |--main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📥 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Plagiarism-Detector-Using-String-Matching.git
```

## Move into Project Folder

```bash
cd Plagiarism-Detector-Using-String-Matching
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

```bash
streamlit run app.py
```

The Streamlit dashboard will automatically open in your browser.

---

# 📝 Sample Input

## Original Document

```text
Artificial Intelligence is transforming many industries.
Machine learning allows systems to learn from data.
Feature engineering can improve prediction accuracy.
Cloud computing provides scalable computing resources.
```

## Submitted Document

```text
Artificial Intelligence is transforming many industries.
Some random content.
Machine learning allows systems to learn from data.
Cloud computing provides scalable computing resources.
```

---

# 📊 Sample Output

```text
Algorithm Used: KMP

Matched Sentences:
1. Artificial Intelligence is transforming many industries.
2. Machine learning allows systems to learn from data.
3. Cloud computing provides scalable computing resources.

Plagiarism Percentage: 75%
```

---

# 📈 Applications

* Academic Integrity Systems
* Assignment Evaluation Platforms
* Research Paper Similarity Analysis
* Content Verification Systems
* EdTech Platforms
* Publishing Platforms
* Documentation Review Tools

---



# 🎓 Learning Outcomes

Through this project I learned:

* String Matching Algorithms
* KMP Algorithm
* Rabin-Karp Algorithm
* Hashing Techniques
* Pattern Searching
* Text Processing
* Streamlit Dashboard Development
* File Handling in Python
* Git and GitHub Project Management
* Real-world Applications of DSA

---

# 🔮 Future Enhancements

* PDF Document Support
* DOCX File Support
* Highlight Copied Text
* Semantic Similarity Detection
* NLP-Based Paraphrase Detection
* Multi-Document Comparison
* Database Integration
* Cloud Deployment

---

# 👨‍💻 Author

**Arshdeep Kaur**

B.Tech Student  | DSA Enthusiast

---

# ⭐ If you found this project useful

Please consider giving the repository a star.
