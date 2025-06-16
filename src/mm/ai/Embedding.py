import os
from functools import cache

from openai import OpenAI
from utils import Log

log = Log("Embedding")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class Embedding:
    MODEL = "text-embedding-3-small"

    @staticmethod
    def round(value: float) -> float:
        return round(value, 4)

    def __init__(self, text_list):
        self.text_list = text_list

    @cache
    def get_idx(self) -> list[str]:
        response = client.embeddings.create(
            input=self.text_list, model=self.MODEL
        )

        idx = {}
        for text, item in zip(self.text_list, response.data):
            idx[text] = [Embedding.round(x) for x in item.embedding]

        n = len(idx)
        log.warning(f"⚠️  Got {n} embeddings for 🤑 {self.MODEL}")
        return idx

    @staticmethod
    def cosine_similarity(emb1, emb2) -> float:

        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        norm1 = sum(a**2 for a in emb1) ** 0.5
        norm2 = sum(b**2 for b in emb2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return Embedding.round(dot_product / (norm1 * norm2))

    @staticmethod
    def get_similarity_matrix(idx1, idx2):
        text_list1 = list(idx1.keys())
        text_list2 = list(idx2.keys())
        n1 = len(text_list1)
        n2 = len(text_list2)

        m = []
        for i1 in range(n1):
            text1 = text_list1[i1]
            emb1 = idx1[text1]
            for i2 in range(n2):
                text2 = text_list2[i2]
                emb2 = idx2[text2]
                sim = Embedding.cosine_similarity(emb1, emb2)
                m.append(((text1, text2), sim))
        m.sort(key=lambda x: x[1], reverse=True)
        return m
