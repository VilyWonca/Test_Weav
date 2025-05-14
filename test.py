import pymupdf4llm

"""Надо разобраться как можно переводить не pdf, а текст старицы в формат маркдовн"""

result = pymupdf4llm.to_markdown("input.pdf")

with open('spamspam.txt', 'w', encoding="utf-8") as f:
    f.write(str(result))

print("Результат сохранен в текст")