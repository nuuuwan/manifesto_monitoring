from utils import Log

from mm.ai import Embedding, EmbIdx
from mm.cabinet_decisions import CabinetDecision
from mm.manifesto import NPPManifestoPDF

log = Log("CompareManifesto")


class CompareManifesto:
    N_LIMIT_CABINET_DECISIONS = 100
    N_LIMIT_MANIFESTO = 100
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
            text = "\n\n".join(
                [
                    f"# {cabinet_decision.title}",
                    f"({cabinet_decision.date_str},"
                    f" {cabinet_decision.decision_num})",
                    f"{cabinet_decision.decision_details}",
                ]
            )

            text_list.append(text)

        idx = emb_idx.multiget(text_list)
        log.info(f"Built EmbIdx for {len(text_list)} cabinet decisions")
        return idx

    def build_emb_idx_for_manifesto(self):
        manifesto = NPPManifestoPDF().get_manifesto()
        all_table = manifesto.all_table
        if self.N_LIMIT_MANIFESTO:
            all_table = all_table[: self.N_LIMIT_MANIFESTO]

        emb_idx = EmbIdx(self.MANIFESTO_ID)
        text_list = []
        for item in all_table:
            text = "\n\n".join(
                [
                    f'# {item["l1_topic"]}',
                    f'## {item["l2_topic"]}',
                    f'### {item["activity"]}',
                    f'{item["item"]}',
                    f'({item["key"]})',
                ]
            )

            text_list.append(text)

        idx = emb_idx.multiget(text_list)
        log.info(f"Built EmbIdx for {len(text_list)} manifesto items")
        return idx

    def get_similarity_matrix(self):
        idx_cabinet_decisions = self.build_emb_idx_for_cabinet_decisions()
        idx_manifesto = self.build_emb_idx_for_manifesto()
        m = Embedding.get_similarity_matrix(
            idx_cabinet_decisions, idx_manifesto
        )
        log.info(f"Got similarity matrix with {len(m)} items")
        return m
