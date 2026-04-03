"""
=============================================================
  Question Bank Validator
  Tests that all questions follow the correct format
  
  HOW TO RUN:  python tests/test_questions.py
=============================================================
"""

import json
import os
import sys

REQUIRED_FIELDS = ['id', 'topic', 'type', 'difficulty', 'question', 'answer', 'explanation']
VALID_TYPES      = ['MCQ', 'TrueFalse', 'ShortAnswer', 'FillBlank']
VALID_DIFFICULTY = ['easy', 'medium', 'hard']

def validate_question_file(filepath):
    """Validate all questions in a JSON file."""
    errors   = []
    warnings = []

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            questions = json.load(f)
        except json.JSONDecodeError as e:
            return [f"JSON parse error: {e}"], []

    if not isinstance(questions, list):
        return ["File must contain a JSON array of questions"], []

    for i, q in enumerate(questions):
        prefix = f"Q[{i+1}] id={q.get('id', 'UNKNOWN')}"

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in q:
                errors.append(f"{prefix}: Missing required field '{field}'")

        # Check type
        if q.get('type') not in VALID_TYPES:
            errors.append(f"{prefix}: Invalid type '{q.get('type')}'. Must be one of {VALID_TYPES}")

        # Check difficulty
        if q.get('difficulty') not in VALID_DIFFICULTY:
            errors.append(f"{prefix}: Invalid difficulty '{q.get('difficulty')}'. Must be one of {VALID_DIFFICULTY}")

        # MCQ-specific checks
        if q.get('type') == 'MCQ':
            if 'options' not in q:
                errors.append(f"{prefix}: MCQ must have 'options' array")
            elif len(q.get('options', [])) < 2:
                errors.append(f"{prefix}: MCQ must have at least 2 options")
            elif q.get('answer') not in q.get('options', []):
                errors.append(f"{prefix}: Answer '{q.get('answer')}' not found in options")

        # TrueFalse check
        if q.get('type') == 'TrueFalse':
            if q.get('answer') not in ['True', 'False']:
                errors.append(f"{prefix}: TrueFalse answer must be 'True' or 'False'")

        # Warnings
        if len(q.get('question', '')) < 10:
            warnings.append(f"{prefix}: Question is very short")
        if len(q.get('explanation', '')) < 20:
            warnings.append(f"{prefix}: Explanation is very short")

    return errors, warnings


def run_all_tests():
    """Run validation on all question files."""
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    questions_dir = os.path.join(script_dir, '..', 'src', 'questions')

    if not os.path.exists(questions_dir):
        print(f"❌ Questions directory not found: {questions_dir}")
        sys.exit(1)

    json_files = [f for f in os.listdir(questions_dir) if f.endswith('.json')]

    if not json_files:
        print("⚠️  No question files found in src/questions/")
        sys.exit(1)

    print("=" * 55)
    print("  ML QUESTION BANK — VALIDATION REPORT")
    print("=" * 55)

    total_questions = 0
    total_errors    = 0
    total_warnings  = 0
    all_passed      = True

    for fname in sorted(json_files):
        fpath  = os.path.join(questions_dir, fname)
        errors, warnings = validate_question_file(fpath)

        with open(fpath, 'r') as f:
            try:
                qs = json.load(f)
                count = len(qs)
            except:
                count = 0

        total_questions += count
        total_errors    += len(errors)
        total_warnings  += len(warnings)

        status = "✅ PASS" if not errors else "❌ FAIL"
        if errors:
            all_passed = False

        print(f"\n  {status}  {fname} ({count} questions)")

        for err in errors:
            print(f"    ❌ ERROR: {err}")
        for warn in warnings:
            print(f"    ⚠️  WARN : {warn}")

        if not errors and not warnings:
            print(f"    ✅ All {count} questions valid")

    print("\n" + "=" * 55)
    print(f"  SUMMARY")
    print(f"  Total questions : {total_questions}")
    print(f"  Total errors    : {total_errors}")
    print(f"  Total warnings  : {total_warnings}")
    print(f"  Status          : {'✅ ALL PASSED' if all_passed else '❌ SOME FAILED'}")
    print("=" * 55)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    run_all_tests()
