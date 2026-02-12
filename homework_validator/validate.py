import os
import sys
import markdown
from pathlib import Path

def check_markdown_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    if len(content.strip()) < 100:
        return False, "Слишком короткое задание (<100 символов)"
    if "# " not in content and "## " not in content:
        return False, "Отсутствуют заголовки"
    return True, "OK"

def main(homework_dir):
    hw_path = Path(homework_dir)
    if not hw_path.exists():
        print("❌ Папка с ДЗ не найдена")
        sys.exit(1)

    md_files = list(hw_path.glob("*.md"))
    if not md_files:
        print("❌ Нет .md файлов в папке")
        sys.exit(1)

    all_ok = True
    for f in md_files:
        ok, msg = check_markdown_file(f)
        status = "✅" if ok else "❌"
        print(f"{status} {f.name}: {msg}")
        if not ok:
            all_ok = False

    if all_ok:
        print("\n🎉 Все домашние задания соответствуют минимальным требованиям!")
        sys.exit(0)
    else:
        print("\n⚠️  Некоторые задания требуют доработки.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python validate.py /путь/к/дз")
        sys.exit(1)
    main(sys.argv[1])