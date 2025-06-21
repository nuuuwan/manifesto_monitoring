from functools import cached_property

from utils import File, Log

from mm.cabinet_decisions import CabinetDecision
from mm.manifesto import NPPManifestoPDF
from mm.monitoring.CompareManifesto import CompareManifesto
from mm.monitoring.ReadMeCompare import ReadMeCompare
from mm.monitoring.ReadMeHeader import ReadMeHeader

log = Log("ReadMe")


class ReadMe(ReadMeHeader, ReadMeCompare):
    README_PATH = "README.md"
    SOURCE_URL = "https://www.npp.lk/up/policies/en/npppolicystatement.pdf"

    def __init__(self):
        self.data_list = CompareManifesto().high_similarity_pairs
        self.manifesto_idx = NPPManifestoPDF().get_manifesto().all_idx
        self.manifesto_to_datalist = {
            x["manifesto_key"]: x for x in self.data_list
        }
        self.cabinet_decision_idx = CabinetDecision.idx()

    @cached_property
    def lines(self):
        return self.header_lines + self.compare_lines

    def build(self):
        File(self.README_PATH).write_lines(self.lines)
        log.info(f"Wrote {self.README_PATH} ({len(self.lines)} lines)")
