import os
import pickle
from functools import cached_property

from utils import Hash, Log

from mm.ai.Embedding import Embedding

log = Log("EmbIdx")


class EmbIdx:
    DIR_EMBEDDING = os.path.join("data", "ai", "embeddings")

    def __init__(self, emb_id: str):
        self.emb_id = emb_id
        self.idx = {}
        self.load()

    @cached_property
    def idx_path(self):
        return os.path.join(self.DIR_EMBEDDING, f"{self.emb_id}.emb_idx.pkl")

    def load(self):
        if not os.path.exists(self.idx_path):
            return {}
        with open(self.idx_path, "rb") as f:
            idx = pickle.load(f)

        n = len(idx)
        log.info(f"Read {n} embs from {self.idx_path}")
        self.idx = idx

    def store(self):
        if not os.path.exists(self.DIR_EMBEDDING):
            os.makedirs(self.DIR_EMBEDDING)
        with open(self.idx_path, "wb") as f:
            pickle.dump(self.idx, f)

        n = len(self.idx)
        file_size = os.path.getsize(self.idx_path)
        file_size_per_emb = file_size / n
        log.info(
            f"Wrote {n} embs to {self.idx_path}"
            f" ({file_size / 1000_000:.1f}MB, "
            f" {file_size_per_emb / 1000:.1f}KB/emb)"
        )

    @staticmethod
    def __hash_text__(text: str) -> str:
        return Hash.md5(text)

    def multiget(self, text_list):
        hot_text_list = [
            text
            for text in text_list
            if self.__hash_text__(text) not in self.idx
        ]
        if hot_text_list:
            hot_idx = Embedding(hot_text_list).get_idx()
            for text in hot_text_list:
                self.idx[self.__hash_text__(text)] = hot_idx[text]

        output_idx = {}
        for text in text_list:
            output_idx[text] = self.idx[self.__hash_text__(text)]

        self.store()
        return output_idx
