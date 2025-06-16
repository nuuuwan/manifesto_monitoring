from utils import Log

from mm.ai import Embedding, EmbIdx
from mm.cabinet_decisions import CabinetDecision

log = Log("CompareManifesto")


class CompareManifesto:
    N_LIMIT_CABINET_DECISIONS = 10
    CABINET_DECISIONS_ID = "cabinet_decisions"
    MANIFESTO_ID = "manifesto"

    def build_emb_idx_for_cabinet_decisions(self):
        cabinet_decisions = CabinetDecision.list_all()
        if self.N_LIMIT_CABINET_DECISIONS:
            cabinet_decisions = cabinet_decisions[
                : self.N_LIMIT_CABINET_DECISIONS
            ]
        emb_idx = EmbIdx(self.CABINET_DECISIONS_ID)
        text_list = []
        for cabinet_decision in cabinet_decisions:
            text = (
                cabinet_decision.title
                + " "
                + cabinet_decision.decision_details
            )
            text_list.append(text)

        idx = emb_idx.multiget(text_list)
        log.info(f"Built EmbIdx for {len(text_list)} cabinet decisions")
        return idx

    def get_most_similar_cabinet_decisions(self):
        idx = self.build_emb_idx_for_cabinet_decisions()

        text_list = list(idx.keys())
        n = len(text_list)
        max_sim = None
        most_similar_pair = None
        for i in range(n - 1):
            text_i = text_list[i]
            emb_i = idx[text_i]
            for j in range(i + 1, n):
                text_j = text_list[j]
                emb_j = idx[text_j]
                sim = Embedding.cosine_similarity(emb_i, emb_j)
                if max_sim is None or sim > max_sim:
                    max_sim = sim
                    most_similar_pair = (text_i, text_j)

        return most_similar_pair, max_sim
