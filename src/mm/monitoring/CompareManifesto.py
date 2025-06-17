from functools import cache

import numpy as np
from utils import Log

from mm.ai import Embedding, EmbIdx
from mm.cabinet_decisions import CabinetDecision
from mm.manifesto import NPPManifestoPDF

log = Log("CompareManifesto")


class CompareManifesto:
    MIN_DATE_CABINET_DECISIONS = "2024-09-24"
    MAX_CABINET_DECISIONS = 1_000
    MAX_MANIFESTO_ITEMS = 2_000
    CABINET_DECISIONS_ID = "cabinet_decisions"
    MANIFESTO_ID = "manifesto"

    @cache
    def build_emb_idx_for_cabinet_decisions(self):
        cabinet_decisions = CabinetDecision.list_all()
        cabinet_decisions = [
            x
            for x in cabinet_decisions
            if x.date_str >= self.MIN_DATE_CABINET_DECISIONS
        ]
        if self.MAX_CABINET_DECISIONS and self.MAX_CABINET_DECISIONS > len(
            cabinet_decisions
        ):
            cabinet_decisions = cabinet_decisions[
                : self.MAX_CABINET_DECISIONS
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
        log.debug(f"Built EmbIdx for {len(text_list)} cabinet decisions")
        return idx

    @cache
    def build_emb_idx_for_manifesto(self):
        manifesto = NPPManifestoPDF().get_manifesto()
        all_table = manifesto.all_table
        if self.MAX_MANIFESTO_ITEMS:
            all_table = all_table[: self.MAX_MANIFESTO_ITEMS]

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
        log.debug(f"Built EmbIdx for {len(text_list)} manifesto items")
        return idx

    @cache
    def get_similarity_matrix(self):
        idx_manifesto = self.build_emb_idx_for_manifesto()
        idx_cabinet_decisions = self.build_emb_idx_for_cabinet_decisions()
        m = Embedding.get_similarity_matrix(
            idx_manifesto, idx_cabinet_decisions
        )
        log.info(f"Got similarity matrix with {len(m)} items")
        return m

    @cache
    def get_high_similarity_pairs(self, min_sim=0.5):
        idx_manifesto = self.build_emb_idx_for_manifesto()
        idx_cabinet_decisions = self.build_emb_idx_for_cabinet_decisions()
        keys1 = list(idx_manifesto.keys())
        keys2 = list(idx_cabinet_decisions.keys())

        m = self.get_similarity_matrix()
        data_list = []
        for i, row in enumerate(m):
            j = np.argmax(row)
            value = row[j]
            if value < min_sim:
                continue
            data = dict(
                manifest_item=keys1[i],
                cabinet_decision=keys2[j],
                similarity=value,
            )
            data_list.append(data)
        log.info(
            f"Found {
                len(data_list)} high similarity pairs with min_sim={min_sim}"
        )
        return data_list
