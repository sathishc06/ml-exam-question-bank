"""
=============================================================
  ML Question Bank — Export to PDF
  ml-exam-question-bank | C. Sathish Kumar
=============================================================

Exports selected questions as a formatted PDF exam paper.

USAGE:
  # Install required package first:
  pip install fpdf2

  # Export 10 questions on logistic regression:
  python examples/export_to_pdf.py --topic logistic_regression --count 10

  # Export full paper with answer key:
  python examples/export_to_pdf.py --topic decision_trees --answers --output DT_paper.pdf

  # Export hard questions only:
  python examples/export_to_pdf.py --difficulty hard --output hard_questions.pdf
=============================================================
"""

import json
import os
import random
import argparse
from datetime import datetime

# ──────────────────────────────────────────────────────────────
# Try to import fpdf2; give helpful install message if missing
# ──────────────────────────────────────────────────────────────
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False


def load_questions(topic=None, difficulty=None, qtype=None, count=None, seed=None):
    """Load and filter questions from JSON files."""
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    questions_dir = os.path.join(script_dir, '..', 'src', 'questions')

    all_questions = []

    if topic:
        fpath = os.path.join(questions_dir, f"{topic}.json")
        if not os.path.exists(fpath):
            available = [f[:-5] for f in os.listdir(questions_dir) if f.endswith('.json')]
            print(f"Topic '{topic}' not found. Available: {available}")
            return []
        with open(fpath, 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
    else:
        for fname in sorted(os.listdir(questions_dir)):
            if fname.endswith('.json'):
                with open(os.path.join(questions_dir, fname), 'r', encoding='utf-8') as f:
                    all_questions.extend(json.load(f))

    if difficulty:
        all_questions = [q for q in all_questions if q.get('difficulty','').lower() == difficulty.lower()]
    if qtype:
        all_questions = [q for q in all_questions if q.get('type','').lower() == qtype.lower()]

    if seed:
        random.seed(seed)
    if count and count < len(all_questions):
        all_questions = random.sample(all_questions, count)

    # Sort: MCQ first, then TrueFalse, then ShortAnswer
    order = {'MCQ': 0, 'TrueFalse': 1, 'ShortAnswer': 2}
    all_questions.sort(key=lambda q: order.get(q.get('type','MCQ'), 3))

    return all_questions


def export_text_fallback(questions, show_answers, output_file):
    """Fallback: export as plain text file if fpdf2 not available."""
    txt_file = output_file.replace('.pdf', '.txt')
    topic_str = questions[0].get('topic','').replace('_',' ').upper() if questions else 'ML'

    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"  MACHINE LEARNING EXAM PAPER — {topic_str}\n")
        f.write(f"  Generated: {datetime.now().strftime('%d-%m-%Y')}\n")
        f.write(f"  Total Questions: {len(questions)}\n")
        f.write("=" * 70 + "\n\n")

        mcq_qs   = [q for q in questions if q.get('type') == 'MCQ']
        tf_qs    = [q for q in questions if q.get('type') == 'TrueFalse']
        short_qs = [q for q in questions if q.get('type') == 'ShortAnswer']

        qn = 1
        if mcq_qs:
            f.write(f"PART A: MULTIPLE CHOICE QUESTIONS  [{len(mcq_qs)} × 2 = {len(mcq_qs)*2} marks]\n")
            f.write("-" * 70 + "\n")
            for q in mcq_qs:
                f.write(f"\n{qn}. {q['question']}\n")
                for i, opt in enumerate(q.get('options',[])):
                    f.write(f"   {chr(65+i)}) {opt}\n")
                if show_answers:
                    f.write(f"   ANSWER: {q['answer']}\n")
                    f.write(f"   EXPLANATION: {q['explanation']}\n")
                qn += 1

        if tf_qs:
            f.write(f"\n\nPART B: TRUE / FALSE  [{len(tf_qs)} × 1 = {len(tf_qs)} marks]\n")
            f.write("-" * 70 + "\n")
            for q in tf_qs:
                f.write(f"\n{qn}. {q['question']}\n")
                f.write("   Answer: _______________\n")
                if show_answers:
                    f.write(f"   ANSWER: {q['answer']}\n")
                qn += 1

        if short_qs:
            f.write(f"\n\nPART C: SHORT ANSWER  [{len(short_qs)} × 5 = {len(short_qs)*5} marks]\n")
            f.write("-" * 70 + "\n")
            for q in short_qs:
                f.write(f"\n{qn}. {q['question']}\n")
                f.write("\n   _________________________________________________________________\n")
                f.write("   _________________________________________________________________\n")
                f.write("   _________________________________________________________________\n")
                if show_answers:
                    f.write(f"\n   ANSWER: {q['answer']}\n")
                qn += 1

        total = len(mcq_qs)*2 + len(tf_qs) + len(short_qs)*5
        f.write(f"\n\n{'='*70}\n  TOTAL MARKS: {total}\n{'='*70}\n")
        f.write("\n  Author: C. Sathish Kumar\n")
        f.write("  Assistant Professor | Biomedical Engineering | IEEE Researcher\n")

    print(f"✅ Exported {len(questions)} questions to: {txt_file}")
    return txt_file


def export_pdf(questions, show_answers, output_file, title="Machine Learning Exam"):
    """Export questions to a properly formatted PDF."""
    if not FPDF_AVAILABLE:
        print("⚠️  fpdf2 library not found. Install with: pip install fpdf2")
        print("   Exporting as .txt file instead...")
        return export_text_fallback(questions, show_answers, output_file)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Header ──
    pdf.set_fill_color(26, 47, 90)       # Navy
    pdf.rect(0, 0, 210, 22, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(10, 6)
    pdf.cell(0, 10, title.upper(), ln=True)

    pdf.set_text_color(200, 150, 12)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(10, 14)
    pdf.cell(0, 6, f"C. Sathish Kumar  |  Generated: {datetime.now().strftime('%d-%m-%Y')}  |  Questions: {len(questions)}", ln=True)

    pdf.set_y(26)
    pdf.set_text_color(30, 30, 30)

    mcq_qs   = [q for q in questions if q.get('type') == 'MCQ']
    tf_qs    = [q for q in questions if q.get('type') == 'TrueFalse']
    short_qs = [q for q in questions if q.get('type') == 'ShortAnswer']
    qn = 1

    def section_header(text):
        pdf.set_fill_color(230, 240, 250)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(26, 47, 90)
        pdf.cell(0, 8, text, fill=True, ln=True)
        pdf.set_text_color(30, 30, 30)
        pdf.ln(2)

    def write_text(text, size=10, bold=False, color=(30,30,30)):
        pdf.set_font("Helvetica", "B" if bold else "", size)
        pdf.set_text_color(*color)
        pdf.multi_cell(0, 5, text)
        pdf.set_text_color(30,30,30)

    if mcq_qs:
        section_header(f"PART A: MULTIPLE CHOICE QUESTIONS  [{len(mcq_qs)} x 2 = {len(mcq_qs)*2} Marks]")
        for q in mcq_qs:
            write_text(f"{qn}. {q['question']}", bold=True, size=10)
            for i, opt in enumerate(q.get('options',[])):
                write_text(f"   {chr(65+i)}) {opt}", size=9)
            if show_answers:
                write_text(f"   Answer: {q['answer']}", size=9, color=(0,100,0))
            pdf.ln(3)
            qn += 1

    if tf_qs:
        section_header(f"PART B: TRUE / FALSE  [{len(tf_qs)} x 1 = {len(tf_qs)} Marks]")
        for q in tf_qs:
            write_text(f"{qn}. {q['question']}", bold=True, size=10)
            if not show_answers:
                write_text("   Answer: _______________", size=9)
            else:
                write_text(f"   Answer: {q['answer']}", size=9, color=(0,100,0))
            pdf.ln(3)
            qn += 1

    if short_qs:
        section_header(f"PART C: SHORT ANSWER  [{len(short_qs)} x 5 = {len(short_qs)*5} Marks]")
        for q in short_qs:
            write_text(f"{qn}. {q['question']}", bold=True, size=10)
            if not show_answers:
                for _ in range(3):
                    write_text("   _______________________________________________________________", size=9, color=(150,150,150))
            else:
                write_text(f"   {q['answer']}", size=9, color=(0,100,0))
            pdf.ln(4)
            qn += 1

    total = len(mcq_qs)*2 + len(tf_qs) + len(short_qs)*5
    pdf.ln(5)
    pdf.set_fill_color(26, 47, 90)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, f"   TOTAL MARKS: {total}", fill=True, ln=True)

    pdf.output(output_file)
    print(f"✅ PDF exported: {output_file}  ({len(questions)} questions, {total} marks)")
    return output_file


def main():
    parser = argparse.ArgumentParser(description='Export ML questions to PDF')
    parser.add_argument('--topic',      type=str, default=None,
                        help='Topic: linear_regression, logistic_regression, decision_trees, kmeans_clustering, neural_networks')
    parser.add_argument('--difficulty', type=str, default=None, help='easy / medium / hard')
    parser.add_argument('--type',       type=str, default=None, help='MCQ / TrueFalse / ShortAnswer')
    parser.add_argument('--count',      type=int, default=None, help='Number of questions')
    parser.add_argument('--output',     type=str, default='exam_paper.pdf', help='Output filename')
    parser.add_argument('--answers',    action='store_true', help='Include answer key')
    parser.add_argument('--seed',       type=int, default=42, help='Random seed for reproducibility')

    args = parser.parse_args()

    questions = load_questions(
        topic=args.topic,
        difficulty=args.difficulty,
        qtype=args.type,
        count=args.count,
        seed=args.seed
    )

    if not questions:
        print("❌  No questions found with the given filters.")
        return

    topic_str = args.topic.replace('_',' ').title() if args.topic else 'Machine Learning'
    title     = f"ML Exam — {topic_str}"
    if args.difficulty:
        title += f" [{args.difficulty.upper()}]"

    export_pdf(questions, show_answers=args.answers, output_file=args.output, title=title)


if __name__ == "__main__":
    main()
