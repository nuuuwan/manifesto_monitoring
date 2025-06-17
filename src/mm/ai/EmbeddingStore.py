import os
import pickle
from functools import cached_property

import numpy as np
from openai import OpenAI
from sklearn.preprocessing import normalize
from utils import Log

log = Log("Embedding")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
log = Log("EmbeddingStore")


class EmbeddingStore:
    MODEL = "text-embedding-3-small"
    DIR_EMBEDDING = os.path.join("data", "ai", "embeddings")

    @staticmethod
    def __get_embedding_matrix__(text_list: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            input=text_list, model=EmbeddingStore.MODEL
        )
        embeddings = [item.embedding for item in response.data]
        n = len(embeddings)
        log.warning(f"⚠️  Got {n} embeddings for 🤑 {EmbeddingStore.MODEL}")
        embedding_matrix = normalize(
            np.array(embeddings, dtype=np.float32), axis=1
        )
        return embedding_matrix

    def __init__(self, emb_id: str, key_to_text: dict[str, str]):
        self.emb_id = emb_id
        self.key_to_text = key_to_text
        self.embedding_matrix = self.__build__()

    @cached_property
    def data_path(self):
        return os.path.join(self.DIR_EMBEDDING, f"{self.emb_id}.emb_idx.pkl")

    def __build__(self) -> list[list[float]]:
        if os.path.exists(self.data_path):
            data = None
            with open(self.data_path, "rb") as f:
                data = pickle.load(f)
            embedding_matrix = data["embedding_matrix"]
        else:
            embedding_matrix = EmbeddingStore.__get_embedding_matrix__(
                list(self.key_to_text.values())
            )
            data = {
                "key_to_text": self.key_to_text,
                "embedding_matrix": embedding_matrix,
            }
            with open(self.data_path, "wb") as f:
                pickle.dump(data, f)

        n = len(embedding_matrix)
        file_size = os.path.getsize(self.data_path)
        file_size_per_emb = file_size / n
        log.debug(
            f"Wrote/Read {n} embs to/from {self.data_path}"
            f" ({file_size / 1000_000:.1f}MB, "
            f" {file_size_per_emb / 1000:.1f}KB/emb)"
        )

        return embedding_matrix
