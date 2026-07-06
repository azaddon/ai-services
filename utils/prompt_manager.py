from pathlib import Path


class PromptManager:

    _cache = {}
    @classmethod
    def get_prompt(cls, file_name: str) -> str:
        if file_name in cls._cache:
            return cls._cache[file_name]
        


        prompt = (Path("prompts") / file_name).read_text(encoding="utf-8")

        cls._cache[file_name] = prompt

        return prompt