import os
import pickle
from functools import cached_property

import numpy as np
import tiktoken
from openai import BadRequestError, OpenAI
from sklearn.preprocessing import normalize
from utils import Hash, Log

log = Log("Embedding")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
log = Log("EmbeddingStore")


class EmbeddingStore:
    MODEL = "text-embedding-3-small"
    MAX_TOKENS_PER_REQUEST = 200_000
    MODEL_URL = (
        "https://platform.openai.com/docs/models/text-embedding-3-small"
    )
    DIR_EMBEDDING = os.path.join("data", "ai", "embeddings")

    @classmethod
    def __get_text_batches__(cls, text_list: list[str]) -> list[list[str]]:
        encoding = tiktoken.encoding_for_model(cls.MODEL)
        batches = []
        batch = []
        batch_token_count = 0

        for text in text_list:
            token_count = len(encoding.encode(text, disallowed_special=()))
            if token_count > cls.MAX_TOKENS_PER_REQUEST:
                raise ValueError(
                    "A single embedding input contains "
                    f"{token_count:,} tokens, exceeding the "
                    f"{cls.MAX_TOKENS_PER_REQUEST:,}-token request limit."
                )

            if (
                batch
                and batch_token_count + token_count
                > cls.MAX_TOKENS_PER_REQUEST
            ):
                batches.append(batch)
                batch = []
                batch_token_count = 0

            batch.append(text)
            batch_token_count += token_count

        if batch:
            batches.append(batch)

        return batches

    @classmethod
    def __get_embeddings__(cls, text_batch: list[str]) -> list[list[float]]:
        try:
            response = client.embeddings.create(
                input=text_batch, model=cls.MODEL
            )
        except BadRequestError as error:
            if (
                error.code != "max_tokens_per_request"
                or len(text_batch) == 1
            ):
                raise

            split_index = len(text_batch) // 2
            return cls.__get_embeddings__(
                text_batch[:split_index]
            ) + cls.__get_embeddings__(text_batch[split_index:])

        return [item.embedding for item in response.data]

    @staticmethod
    def __get_embedding_matrix__(text_list: list[str]) -> list[list[float]]:
        embeddings = []
        for text_batch in EmbeddingStore.__get_text_batches__(text_list):
            embeddings.extend(
                EmbeddingStore.__get_embeddings__(text_batch)
            )

        n = len(embeddings)
        log.warning(f"⚠️  Got {n} embeddings for 🤑 {EmbeddingStore.MODEL}")
        embedding_matrix = normalize(
            np.array(embeddings, dtype=np.float32), axis=1
        )
        return embedding_matrix

    def __init__(self, emb_id: str, key_to_text: dict[str, str]):
        self.emb_id = emb_id
        self.key_to_text = key_to_text
        self.hash = Hash.md5(str(self.key_to_text))[:6]
        self.embedding_matrix = self.__build__()

    @cached_property
    def data_path(self):
        return os.path.join(
            self.DIR_EMBEDDING, f"{self.emb_id}.{self.hash}.pkl"
        )

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
