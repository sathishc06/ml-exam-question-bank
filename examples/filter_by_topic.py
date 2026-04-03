"""
=============================================================
  ML Question Bank — Filter by Topic / Difficulty / Type
  ml-exam-question-bank | C. Sathish Kumar
=============================================================

USAGE:
  # Show all questions for a topic
  python examples/filter_by_topic.py --topic decision_trees

  # Show only hard MCQ questions from logistic regression
  python examples/filter_by_topic.py --topic logistic_regression --difficulty hard --type MCQ

  # Show all short answer questions across all topics
  python examples/filter_by_topic.py --type ShortAnswer

  # List all available topics and question counts
  python examples/filter_by_topic.py --summary
=============================================================
"""

import json
import os
import argparse


def load_all_questions(topic=None):
    """Load questions from JSON files."""
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    questions_dir = os.path.join(script_dir, '..', 'src', 'questions')

    all_questions = []

    if topic:
        fpath = os.path.join(questions_dir, f"{topic}.json")
        if not os.path.exists(fpath):
            available = [f[:-5] for f in os.listdir(questions_dir) if f.endswith('.json')]
            print(f"❌  Topic '{topic}' not found.")
            print(f"   Available topics: {available}")
            return []
        with open(fpath, 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
    else:
        for fname in sorted(os.listdir(questions_dir)):
            if fname.endswith('.json'):
                with open(os.path.join(questions_dir, fname), 'r', encoding='utf-8') as f:
                    all_questions.extend(json.load(f))

    return all_questions


def show_summary():
    """Show summary of all topics and question counts."""
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    questions_dir = os.path.join(script_dir, '..', 'src', 'questions')

    print("\n" + "=" * 65)
    print("  ML QUESTION BANK — SUMMARY")
    print("=" * 65)
    print(f"\n  {'Topic':<30} {'Total':>7} {'Easy':>6} {'Medium':>8} {'Hard':>6}")
    print("  " + "-" * 60)

    grand_total = 0
    for fname in sorted(os.listdir(questions_dir)):
        if fname.endswith('.json'):
            topic = fname[:-5]
            with open(os.path.join(questions_dir, fname), 'r', encoding='utf-8') as f:
                qs = json.load(f)
            total  = len(qs)
            easy   = sum(1 for q in qs if q.get('difficulty') == 'easy')
            medium = sum(1 for q in qs if q.get('difficulty') == 'medium')
            hard   = sum(1 for q in qs if q.get('difficulty') == 'hard')
            grand_total += total
            print(f"  {topic:<30} {total:>7} {easy:>6} {medium:>8} {hard:>6}")

    print("  " + "-" * 60)
    print(f"  {'TOTAL':<30} {grand_total:>7}")

    # Type breakdown
    all_qs = load_all_questions()
    mcq    = sum(1 for q in all_qs if q.get('type') == 'MCQ')
    tf     = sum(1 for q in all_qs if q.get('type') == 'TrueFalse')
    short  = sum(1 for q in all_qs if q.get('type') == 'ShortAnswer')

    print(f"\n  Question Types:  MCQ={mcq}  TrueFalse={tf}  ShortAnswer={short}")
    print("=" * 65 + "\n")


def print_questions(questions, show_answers=True):
    """Print filtered questions with formatting."""
    if not questions:
        print("\n  ⚠️  No questions match your filters.\n")
        return

    type_icons = {'MCQ': '🔵', 'TrueFalse': '🟡', 'ShortAnswer': '🟢'}
    diff_icons = {'easy': '⭐', 'medium': '⭐⭐', 'hard': '⭐⭐⭐'}

    print("\n" + "=" * 65)
    print(f"  FILTERED QUESTIONS  ({len(questions)} results)")
    print("=" * 65)

    for i, q in enumerate(questions, 1):
        t_icon = type_icons.get(q.get('type',''), '⚪')
        d_icon = diff_icons.get(q.get('difficulty',''), '')
        topic  = q.get('topic','').replace('_',' ').upper()

        print(f"\n  [{i}] {t_icon} [{q.get('type','')}] {d_icon}  ID: {q.get('id','')}")
        print(f"      Topic: {topic}")
        print(f"\n      Q: {q['question']}")

        if q.get('type') == 'MCQ' and 'options' in q:
            for j, opt in enumerate(q['options']):
                print(f"         {chr(65+j)}) {opt}")

        if show_answers:
            print(f"\n      ✅ Answer: {q['answer']}")
            print(f"      💡 {q['explanation']}")

        print("  " + "-" * 60)

    print(f"\n  Total: {len(questions)} questions\n")


def main():
    parser = argparse.ArgumentParser(
        description='Filter ML exam questions by topic, difficulty, or type',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python filter_by_topic.py --summary
  python filter_by_topic.py --topic linear_regression
  python filter_by_topic.py --topic kmeans_clustering --difficulty hard
  python filter_by_topic.py --type ShortAnswer
  python filter_by_topic.py --difficulty easy --no-answers
        """
    )
    parser.add_argument('--topic',      type=str, default=None,
                        help='Topic name: linear_regression, logistic_regression, decision_trees, kmeans_clustering, neural_networks')
    parser.add_argument('--difficulty', type=str, default=None,
                        help='Difficulty: easy, medium, hard')
    parser.add_argument('--type',       type=str, default=None,
                        help='Question type: MCQ, TrueFalse, ShortAnswer')
    parser.add_argument('--summary',    action='store_true',
                        help='Show topic summary and exit')
    parser.add_argument('--no-answers', action='store_true',
                        help='Hide answers (question-only mode)')

    args = parser.parse_args()

    if args.summary:
        show_summary()
        return

    questions = load_all_questions(topic=args.topic)

    if args.difficulty:
        questions = [q for q in questions if q.get('difficulty','').lower() == args.difficulty.lower()]

    if args.type:
        questions = [q for q in questions if q.get('type','').lower() == args.type.lower()]

    print_questions(questions, show_answers=not args.no_answers)


if __name__ == "__main__":
    main()
