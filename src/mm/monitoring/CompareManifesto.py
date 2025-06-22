from functools import cached_property

import numpy as np
from utils import Log

from mm.ai import EmbeddingStore
from mm.cabinet_decisions import CabinetDecision
from mm.manifesto import NPPManifestoPDF

log = Log("CompareManifesto")


class CompareManifesto:
    MIN_DATE_CABINET_DECISIONS = "2024-09-24"
    MAX_CABINET_DECISIONS = 2000
    MAX_MANIFESTO_ITEMS = 2000

    VERSION_ID = "prod-v3"
    CABINET_DECISIONS_ID = f"cabinet_decisions-{VERSION_ID}"
    MANIFESTO_ID = f"manifesto-{VERSION_ID}"

    @cached_property
    def cabinet_decisions_for_compare(self):
        cabinet_decisions = CabinetDecision.list_all()
        cabinet_decisions = [
            x
            for x in cabinet_decisions
            if x.date_str >= self.MIN_DATE_CABINET_DECISIONS
        ]
        if self.MAX_CABINET_DECISIONS and self.MAX_CABINET_DECISIONS < len(
            cabinet_decisions
        ):
            cabinet_decisions = cabinet_decisions[
                : self.MAX_CABINET_DECISIONS
            ]

        return cabinet_decisions

    @cached_property
    def n_cabinet_decisions(self):
        return len(self.cabinet_decisions_for_compare)

    @cached_property
    def cabinet_decisions_key_to_text(self):
        key_to_text = {}
        for cabinet_decision in self.cabinet_decisions_for_compare:
            text = "\n\n".join(
                [
                    f"# {cabinet_decision.title}",
                    f"{cabinet_decision.decision_details}",
                ]
            )
            key = cabinet_decision.key
            key_to_text[key] = text

        return key_to_text

    @cached_property
    def cabinet_decisions_embedding_store(self):
        embedding_store = EmbeddingStore(
            emb_id=self.CABINET_DECISIONS_ID,
            key_to_text=self.cabinet_decisions_key_to_text,
        )
        return embedding_store

    @cached_property
    def manifesto_items(self):
        manifesto = NPPManifestoPDF().get_manifesto()
        all_table = manifesto.all_table
        if self.MAX_MANIFESTO_ITEMS:
            all_table = all_table[: self.MAX_MANIFESTO_ITEMS]

        return all_table

    @cached_property
    def n_manifesto_items(self):
        return len(self.manifesto_items)

    @cached_property
    def manifesto_key_to_text(self):
        all_table = self.manifesto_items
        key_to_text = {}
        for item in all_table:
            key = item["key"]
            text = "\n\n".join(
                [
                    f'### {item["activity"]}',
                    f'{item["item"]}',
                ]
            )
            key_to_text[key] = text

        return key_to_text

    @cached_property
    def manifesto_embedding_store(self):
        embedding_store = EmbeddingStore(
            emb_id=self.MANIFESTO_ID,
            key_to_text=self.manifesto_key_to_text,
        )
        return embedding_store

    @cached_property
    def similarity_matrix(self):
        manifesto_es = self.manifesto_embedding_store
        cabinet_decisions_es = self.cabinet_decisions_embedding_store
        mat1 = manifesto_es.embedding_matrix
        mat2 = cabinet_decisions_es.embedding_matrix
        similarity_matrix = np.dot(mat1, mat2.T)
        return similarity_matrix

    @cached_property
    def similarity_data_list(self):
        items_i = list(self.manifesto_key_to_text.items())
        items_j = list(self.cabinet_decisions_key_to_text.items())
        m = self.similarity_matrix
        data_list = []
        for i, row in enumerate(m):
            j = np.argmax(row)
            value = row[j]

            data = dict(
                i=i,
                j=j,
                manifesto_key=items_i[i][0],
                manifesto_text=items_i[i][1],
                cabinet_decision_key=items_j[j][0],
                cabinet_decision_text=items_j[j][1],
                similarity=float(value),
            )
            data_list.append(data)

        data_list.sort(key=lambda x: x["similarity"], reverse=True)
        log.info(f"Found {len(data_list)} similarity data items")
        return data_list
