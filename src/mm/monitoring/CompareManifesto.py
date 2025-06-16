from utils import Log

from mm.ai import EmbIdx
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
