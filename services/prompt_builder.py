
class PromptBuild():
    def __init__(self):
        pass

    def build_prompt(self, chunks_dict: list[dict], quary: str):

        prompt = f"""Ты — интеллектуальный ассистент. Отвечай на вопрос, используя исключительно предоставленный контекст.
                    Не выдумывай информацию и не ссылайся на внешний опыт. Если контекста недостаточно — так и скажи. 

                    Контекст:
                    {chunks_dict}

                    Вопрос:
                    {quary}

                    Ответ:
                  """
        return prompt