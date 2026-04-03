"""
=============================================================
  ML Exam Question Bank — Quiz Generator
  ml-exam-question-bank | C. Sathish Kumar
=============================================================

USAGE:
  python examples/generate_quiz.py
  python examples/generate_quiz.py --topic linear_regression --count 5
  python examples/generate_quiz.py --topic logistic_regression --difficulty hard
  python examples/generate_quiz.py --type MCQ --count 10

DESCRIPTION:
  Randomly generates a quiz paper from the question bank.
  Outputs formatted questions ready to print or use in exams.
=============================================================
"""

import json
import random
import os
import argparse
from datetime import datetime

def load_questions(topic=None, question_type=None, difficulty=None):
    """Load questions from JSON files based on filters."""
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    questions_dir = os.path.join(script_dir, '..', 'src', 'questions')

    all_questions = []

    # Load all or specific topic files
    if topic:
        file_path = os.path.join(questions_dir, f"{topic}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                all_questions.extend(json.load(f))
        else:
            print(f"⚠️  No question file found for topic: {topic}")
            print(f"   Available: {[f[:-5] for f in os.listdir(questions_dir) if f.endswith('.json')]}")
            return []
    else:
        for fname in os.listdir(questions_dir):
            if fname.endswith('.json'):
                with open(os.path.join(questions_dir, fname), 'r', encoding='utf-8') as f:
                    all_questions.extend(json.load(f))

    # Apply filters
    if question_type:
        all_questions = [q for q in all_questions if q.get('type','').lower() == question_type.lower()]
    if difficulty:
        all_questions = [q for q in all_questions if q.get('difficulty','').lower() == difficulty.lower()]

    return all_questions


def print_quiz(questions, show_answers=False, title="MACHINE LEARNING QUIZ"):
    """Print formatted quiz paper."""
    print("\n" + "=" * 65)
    print(f"  {title}")
    print(f"  Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    print(f"  Total Questions: {len(questions)}")
    print("=" * 65)

    # Group by type
    mcq_qs    = [q for q in questions if q.get('type') == 'MCQ']
    tf_qs     = [q for q in questions if q.get('type') == 'TrueFalse']
    short_qs  = [q for q in questions if q.get('type') == 'ShortAnswer']

    q_num = 1

    if mcq_qs:
        print(f"\n{'─'*65}")
        print(f"  PART A: MULTIPLE CHOICE QUESTIONS")
        print(f"  (Choose the correct answer)          [{len(mcq_qs)} × 2 = {len(mcq_qs)*2} marks]")
        print(f"{'─'*65}")
        for q in mcq_qs:
            difficulty_tag = {"easy": "★", "medium": "★★", "hard": "★★★"}.get(q.get('difficulty',''), "")
            print(f"\n  {q_num}. [{q.get('topic','').replace('_',' ').upper()}] {difficulty_tag}")
            print(f"     {q['question']}")
            for i, opt in enumerate(q.get('options', [])):
                label = chr(65 + i)  # A, B, C, D
                print(f"       {label}) {opt}")
            if show_answers:
                print(f"     ✅ Answer: {q['answer']}")
                print(f"     💡 {q['explanation']}")
            q_num += 1

    if tf_qs:
        print(f"\n{'─'*65}")
        print(f"  PART B: TRUE / FALSE")
        print(f"  (Write True or False)                [{len(tf_qs)} × 1 = {len(tf_qs)} marks]")
        print(f"{'─'*65}")
        for q in tf_qs:
            print(f"\n  {q_num}. {q['question']}")
            print(f"     Answer: _______________")
            if show_answers:
                print(f"     ✅ Answer: {q['answer']}")
                print(f"     💡 {q['explanation']}")
            q_num += 1

    if short_qs:
        print(f"\n{'─'*65}")
        print(f"  PART C: SHORT ANSWER QUESTIONS")
        print(f"  (Answer in 3-5 sentences)            [{len(short_qs)} × 5 = {len(short_qs)*5} marks]")
        print(f"{'─'*65}")
        for q in short_qs:
            print(f"\n  {q_num}. {q['question']}")
            print()
            print(f"     ____________________________________________________________")
            print(f"     ____________________________________________________________")
            print(f"     ____________________________________________________________")
            if show_answers:
                print(f"     ✅ Answer: {q['answer']}")
            q_num += 1

    total = len(mcq_qs)*2 + len(tf_qs)*1 + len(short_qs)*5
    print(f"\n{'='*65}")
    print(f"  TOTAL MARKS: {total}")
    print(f"{'='*65}\n")


def main():
    parser = argparse.ArgumentParser(description='ML Question Bank Quiz Generator')
    parser.add_argument('--topic', type=str, default=None,
                        help='Topic: linear_regression, logistic_regression, decision_trees, kmeans_clustering')
    parser.add_argument('--count', type=int, default=10,
                        help='Number of questions (default: 10)')
    parser.add_argument('--difficulty', type=str, default=None,
                        help='Difficulty: easy, medium, hard')
    parser.add_argument('--type', type=str, default=None,
                        help='Type: MCQ, TrueFalse, ShortAnswer')
    parser.add_argument('--answers', action='store_true',
                        help='Show answers (answer key mode)')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducible quizzes')

    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)

    # Load questions
    questions = load_questions(
        topic=args.topic,
        question_type=args.type,
        difficulty=args.difficulty
    )

    if not questions:
        print("❌ No questions found with the given filters.")
        return

    # Sample questions
    n = min(args.count, len(questions))
    selected = random.sample(questions, n)

    # Sort by type for clean output: MCQ, TrueFalse, ShortAnswer
    type_order = {'MCQ': 0, 'TrueFalse': 1, 'ShortAnswer': 2}
    selected.sort(key=lambda q: type_order.get(q.get('type', 'MCQ'), 3))

    # Build title
    topic_str = args.topic.replace('_', ' ').title() if args.topic else 'All Topics'
    diff_str  = f" [{args.difficulty.upper()}]" if args.difficulty else ""
    title     = f"ML QUIZ — {topic_str}{diff_str}"

    print_quiz(selected, show_answers=args.answers, title=title)

    if not args.answers:
        print("  💡 TIP: Run with --answers flag to see the answer key")
        print(f"  Example: python examples/generate_quiz.py --topic {args.topic or 'linear_regression'} --answers\n")


if __name__ == "__main__":
    main()
