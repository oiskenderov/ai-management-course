import os
import sys
import json
import re
from pathlib import Path

# Загружаем эталонные ответы
with open("./answer_keys.json", "r", encoding="utf-8") as f:
    ANSWER_KEYS = json.load(f)

def extract_answers_from_md(content: str):
    """Извлекает ответы из Markdown в формате > Ответ: X"""
    answers = {}
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        match = re.search(r"^\s*>?\s*Ответ:\s*([a-e])\s*$", line, re.IGNORECASE)
        if match:
            q_num = len(answers) + 1
            answers[f"q{q_num}"] = match.group(1).lower()
    return answers

def grade_submission(file_path: Path, lesson_key: str = "lesson_01"):
    content = file_path.read_text(encoding="utf-8")
    student_answers = extract_answers_from_md(content)
    expected = ANSWER_KEYS.get(lesson_key, {})
    
    correct = 0
    total = len(expected)
    feedback = []

    for q, expected_ans in expected.items():
        student_ans = student_answers.get(q, None)
        if student_ans == expected_ans:
            correct += 1
            feedback.append(f"✅ {q}: верно")
        else:
            feedback.append(f"❌ {q}: ожидалось '{expected_ans}', получено '{student_ans}'")

    score = correct / total if total > 0 else 0
    return score, feedback

def main(homework_dir):
    hw_path = Path(homework_dir)
    if not hw_path.exists():
        print("❌ Папка с ДЗ не найдена")
        sys.exit(1)

    md_files = list(hw_path.glob("*.md"))
    if not md_files:
        print("❌ Нет .md файлов в папке")
        sys.exit(1)

    for f in md_files:
        print(f"\n📄 Проверка: {f.name}")
        try:
            # Определяем занятие по имени файла (например, orkhan_hw1.md → lesson_01)
            lesson_key = "lesson_01"  # можно улучшить логику
            score, feedback = grade_submission(f, lesson_key)
            for line in feedback:
                print(line)
            print(f"📊 Итог: {int(score * 100)}% правильных ответов")
        except Exception as e:
            print(f"⚠️ Ошибка при проверке {f.name}: {e}")

    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python validate.py /путь/к/дз")
        sys.exit(1)
    main(sys.argv[1])