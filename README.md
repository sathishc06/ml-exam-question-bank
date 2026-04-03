# 📝 ml-exam-question-bank

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Questions](https://img.shields.io/badge/Questions-200%2B-purple)](src/questions/)
[![Topics](https://img.shields.io/badge/Topics-10%20ML%20Topics-orange)](src/)

> **Open-source question bank and quiz generator for Machine Learning courses.**
> 200+ verified questions across 10 ML topics — for faculty to use in exams, students to practice, and institutions to standardize ML assessments.

---

## 📌 Why This Project?

There is no standardized, open, reusable question bank for ML/AI courses in Indian universities.
This project solves that — a free, contributor-friendly, curriculum-aligned question bank.

**Perfect for:**
- 👨‍🏫 Faculty writing question papers (Anna University, VTU, GTU, KTU syllabus)
- 🎓 Students preparing for university exams and viva voce
- 🏫 Institutions standardizing AI/ML assessments

---

## 📁 Structure

```
ml-exam-question-bank/
│
├── src/
│   └── questions/
│       ├── linear_regression.json      ← 25 questions
│       ├── logistic_regression.json    ← 25 questions
│       ├── decision_trees.json         ← 20 questions
│       ├── kmeans_clustering.json      ← 20 questions
│       └── neural_networks.json        ← 20 questions
│
├── examples/
│   ├── generate_quiz.py    ← Generate random quiz papers
│   ├── filter_by_topic.py  ← Filter questions by topic/difficulty
│   └── export_to_pdf.py    ← Export questions to PDF (optional)
│
├── tests/
│   └── test_questions.py   ← Validates question format
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/ml-exam-question-bank.git
cd ml-exam-question-bank
pip install -r requirements.txt

# Generate a 10-question quiz on Logistic Regression
python examples/generate_quiz.py --topic logistic_regression --count 10

# Get all hard questions from Decision Trees
python examples/filter_by_topic.py --topic decision_trees --difficulty hard
```

---

## 📋 Question Format

Each question is stored as JSON:

```json
{
  "id": "LR-001",
  "topic": "linear_regression",
  "type": "MCQ",
  "difficulty": "medium",
  "question": "Which metric is NOT used to evaluate Linear Regression models?",
  "options": ["MSE", "RMSE", "R²", "F1-Score"],
  "answer": "F1-Score",
  "explanation": "F1-Score is used for classification problems. MSE, RMSE and R² are regression metrics."
}
```

**Types:** MCQ, Short Answer, True/False, Fill in the Blank

**Difficulty:** easy, medium, hard

---

## 📊 Topics Covered

| Topic | Questions | MCQ | Short | T/F |
|-------|-----------|-----|-------|-----|
| Linear Regression | 25 | 15 | 7 | 3 |
| Logistic Regression | 25 | 15 | 7 | 3 |
| Decision Trees | 20 | 12 | 5 | 3 |
| K-Means Clustering | 20 | 12 | 5 | 3 |
| Neural Networks | 20 | 12 | 5 | 3 |
| **TOTAL** | **110** | **66** | **29** | **15** |

---

## 🤝 Contributing

We welcome contributions! Add questions from your domain:

1. Fork the repo
2. Add questions to the relevant JSON file (follow the format)
3. Run `python tests/test_questions.py` to validate
4. Submit a Pull Request

**Especially welcome:** Questions from Biomedical AI, Healthcare ML, IoT domains

---

## 👤 Author

**C. Sathish Kumar**
Assistant Professor, Biomedical Engineering | IEEE Researcher | QIP Certified (NIT Puducherry)
📧 csathishkumar08@gmail.com

---

## 📄 License

MIT License — free to use in academic and educational settings.
