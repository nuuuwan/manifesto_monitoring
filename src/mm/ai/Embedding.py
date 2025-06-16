import os
from functools import cached_property

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class Embedding:
    MODEL = "text-embedding-3-small"

    def __init__(self, text_list):
        self.text_list = text_list

    @cached_property
    def embedding(self) -> list[str]:
        response = client.embeddings.create(
            input=self.text_list, model=self.MODEL
        )
        return [item.embedding for item in response.data]
