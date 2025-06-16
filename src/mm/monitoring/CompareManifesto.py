import os

from utils import JSONFile, Log

from mm.cabinet_decisions import CabinetDecision

log = Log("CompareManifesto")


class CompareManifesto:
    N_LIMIT_CABINET_DECISIONS = 10
    DIR_EMBEDDING = os.path.join("data", "ai", "embeddings")
    CABINET_DECISION_EMB_IDX_PATH = os.path.join(
        DIR_EMBEDDING, "cabinet_decision_embedding.json"
    )

    def load_cabinet_decision_emb_idx(self):
        if not os.path.exists(self.CABINET_DECISION_EMB_IDX_PATH):
            return {}
        emb_idx = JSONFile(self.CABINET_DECISION_EMB_IDX_PATH).read()
        n = len(emb_idx)
        log.info(f"Read {n} embs from {self.CABINET_DECISION_EMB_IDX_PATH}")

    def store_cabinet_decision_emb_idx(self, emb_idx):
        JSONFile(self.CABINET_DECISION_EMB_IDX_PATH).write(emb_idx)
        n = len(emb_idx)
        log.info(f"Wrote {n} embs to {self.CABINET_DECISION_EMB_IDX_PATH}")

    def build_embedding_for_cabinet_decisions(self):
        cabinet_decisions = CabinetDecision.list_all()
        if self.N_LIMIT_CABINET_DECISIONS:
            cabinet_decisions = cabinet_decisions[
                : self.N_LIMIT_CABINET_DECISIONS
            ]
