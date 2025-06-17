import os
from functools import cache

import numpy as np
from openai import OpenAI
from sklearn.preprocessing import normalize
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
        mat1 = list(idx1.values())
        mat2 = list(idx2.values())
        mat1 = normalize(np.array(mat1, dtype=np.float32), axis=1)
        mat2 = normalize(np.array(mat2, dtype=np.float32), axis=1)
        similarity_matrix = np.dot(mat1, mat2.T)

        return similarity_matrix
