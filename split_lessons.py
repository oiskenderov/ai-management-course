import re
from pathlib import Path

SOURCE = "./Course_full.md"
OUTPUT_DIR = Path("ai-management-course")

text = Path(SOURCE).read_text(encoding="utf-8")

lessons = re.split(r"## 📘 \*\*Занятие (\d+):", text)

for i in range(1, len(lessons), 2):
    lesson_num = lessons[i]
    lesson_body = lessons[i+1]

    lesson_path = OUTPUT_DIR / f"lesson-{lesson_num.zfill(2)}"
    lesson_path.mkdir(parents=True, exist_ok=True)

    # Split sections
    presentation = re.search(r"### 🖥️ \*\*Презентация.*?(?=### 📚)", lesson_body, re.S)
    methodology = re.search(r"### 📚 \*\*Методическое пособие.*?(?=### 🧪)", lesson_body, re.S)
    test = re.search(r"### 🧪 \*\*Тест.*", lesson_body, re.S)

    if presentation:
        (lesson_path / "presentation.md").write_text(presentation.group(), encoding="utf-8")

    if methodology:
        (lesson_path / "methodology.md").write_text(methodology.group(), encoding="utf-8")

    if test:
        (lesson_path / "test.md").write_text(test.group(), encoding="utf-8")

print("Lessons successfully split.")
