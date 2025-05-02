
class PromptBuild():
    def __init__(self):
        pass

    def build_prompt(self, chunks_list: list[str], quary: str):
        chunks = "\n\n".join(chunks_list)
        prompt = f"""Ты — интеллектуальный ассистент. Отвечай на вопрос, используя исключительно предоставленный контекст.
                    Не выдумывай информацию и не ссылайся на внешний опыт. Если контекста недостаточно — так и скажи. 

                    Контекст:
                    {chunks}

                    Вопрос:
                    {quary}

                    Ответ:
                  """
        return prompt