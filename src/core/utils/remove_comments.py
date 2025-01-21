import argparse
import re


def remove_comments(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            # Удаляем строки, начинающиеся с #
            if not re.match(r"^\s*#", line):
                file.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove comments from a Python file.")
    parser.add_argument("file_path", help="Path to the file to process")
    args = parser.parse_args()

    remove_comments(args.file_path)
